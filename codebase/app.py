import os
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import streamlit as st
from core import SAMPLES, analyze, fingerprint, render_final, audit_payload
from agent.model import analyze_script_ai, get_api_key

CLICKABLE_SCRIPT_CSS = """
.script-paper {
    color: #1d3635;
    font: 1.08rem/2.1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #fff;
    border: 1px solid #dce4df;
    border-radius: 12px;
    padding: 1.7rem;
    height: 420px;
    max-height: 420px;
    box-sizing: border-box;
    overflow-y: auto;
    overscroll-behavior: contain;
    scrollbar-gutter: stable;
    scrollbar-width: thin;
    scrollbar-color: #9aaca6 #f2f5f2;
    overflow-wrap: anywhere;
}
.script-paper::-webkit-scrollbar { width: 10px; }
.script-paper::-webkit-scrollbar-track { background: #f2f5f2; border-radius: 999px; }
.script-paper::-webkit-scrollbar-thumb { background: #9aaca6; border: 2px solid #f2f5f2; border-radius: 999px; }
.script-paper::-webkit-scrollbar-thumb:hover { background: #6f8880; }
.finding-link {
    appearance: none;
    border: 0;
    border-radius: 3px;
    padding: 2px 1px;
    color: #4a3c16;
    background: #f6e9bf;
    font: inherit;
    line-height: inherit;
    text-align: left;
    cursor: pointer;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}
.finding-link.accept { background: #deeee5; color: #20533b; }
.finding-link.keep { background: #ebeeec; color: #4a5550; }
.finding-link.selected { outline: 2px solid #a37c23; outline-offset: 2px; }
.finding-link:hover { box-shadow: inset 0 -2px 0 #a37c23; }
.finding-link:focus-visible { outline: 3px solid #a37c23; outline-offset: 3px; }
@media (max-width: 700px) { .script-paper { padding: 1.1rem; } }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

REVIEW_SCRIPT_HEIGHT = 420

CLICKABLE_SCRIPT_JS = """
export default function(component) {
    const { data, setTriggerValue, parentElement } = component;
    const root = parentElement.querySelector('[data-script-root]');
    root.innerHTML = data.html;

    const activeFinding = root.querySelector('.finding-link.selected');
    if (activeFinding) {
        requestAnimationFrame(() => {
            const rootRect = root.getBoundingClientRect();
            const findingRect = activeFinding.getBoundingClientRect();
            const targetTop = root.scrollTop
                + findingRect.top - rootRect.top
                - (root.clientHeight - findingRect.height) / 2;
            root.scrollTo({
                top: Math.max(0, targetTop),
                behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
            });
        });
    }

    const buttons = root.querySelectorAll('[data-finding-id]');
    const handlers = [];
    buttons.forEach((button) => {
        const handler = () => {
            setTriggerValue('selected', `${button.dataset.findingId}|${Date.now()}`);
        };
        button.addEventListener('click', handler);
        handlers.push([button, handler]);
    });

    return () => handlers.forEach(([button, handler]) => {
        button.removeEventListener('click', handler);
    });
}
"""

clickable_script = st.components.v2.component(
    "clickable_script_findings",
    html='<div class="script-paper" data-script-root aria-label="Kịch bản có các đoạn cần duyệt"></div>',
    css=CLICKABLE_SCRIPT_CSS,
    js=CLICKABLE_SCRIPT_JS,
)

st.set_page_config(page_title="TechScript QA · Biên tập để nói", page_icon="✳", layout="wide", initial_sidebar_state="collapsed")
st.html(f"<style>{Path(__file__).with_name('styles.css').read_text(encoding='utf-8')}</style>")

is_test = bool(os.environ.get("STREAMLIT_TESTING"))
has_key = bool(get_api_key())
default_engine = "Mẫu đối chuẩn CP2 (Mock)" if (is_test or not has_key) else "AI Thật (GPT-4o-mini)"

s = st.session_state
for key, value in {
    "stage": "input", 
    "source": SAMPLES["Demo tính năng · Dev / BA"], 
    "audience": "Đồng nghiệp ít chuyên môn kỹ thuật", 
    "findings": [], 
    "decisions": {}, 
    "events": [], 
    "covered": False, 
    "run_hash": "", 
    "run_count": 0,
    "engine_mode": default_engine
}.items():
    if key not in s:
        s[key] = value

# Keep the source/context when their widgets are absent on later steps.
s.source = s.source
s.audience = s.audience

def invalidate():
    s.stage = "input"
    s.findings = []
    s.decisions = {}
    s.events = []
    s.run_hash = ""

def load_sample():
    s.source = SAMPLES[s.sample]
    invalidate()

def event(finding, action, replacement=""):
    s.decisions[finding.id] = {"action": action, "replacement": replacement}
    s.events.append({"at": datetime.now(timezone.utc).isoformat(), "finding_id": finding.id, "action": action, "replacement": replacement})

def queue_next_pending(findings, current_index):
    """Move forward through pending findings, then wrap to any earlier pending item."""
    ordered = list(range(current_index + 1, len(findings))) + list(range(0, current_index))
    next_index = next((index for index in ordered if findings[index].id not in s.decisions), None)
    if next_index is not None:
        s[f"queued_pick_{s.run_count}"] = next_index

def document_html(source, findings, active=None):
    chunks, cursor = [], 0
    for item in findings:
        chunks.append(escape(source[cursor:item.start]))
        state = s.decisions.get(item.id, {}).get("action", "pending")
        css = state + (" selected" if item.id == active else "")
        chunks.append(f'<mark class="{css}" title="{escape(item.category)}">{escape(item.original)}</mark>')
        cursor = item.end
    chunks.append(escape(source[cursor:]))
    return '<div class="script-paper">' + ''.join(chunks).replace('\n', '<br>') + '</div>'

def clickable_document_html(source, findings, active=None):
    """Return escaped, trusted markup for the interactive script component."""
    chunks, cursor = [], 0
    for index, item in enumerate(findings):
        chunks.append(escape(source[cursor:item.start]))
        state = s.decisions.get(item.id, {}).get("action", "pending")
        css = state + (" selected" if item.id == active else "")
        label = escape(f"Mở gợi ý {index + 1}: {item.original}", quote=True)
        finding_id = escape(str(item.id), quote=True)
        chunks.append(
            f'<button type="button" class="finding-link {css}" '
            f'data-finding-id="{finding_id}" aria-label="{label}" '
            f'aria-pressed="{"true" if item.id == active else "false"}">'
            f'{escape(item.original)}</button>'
        )
        cursor = item.end
    chunks.append(escape(source[cursor:]))
    return ''.join(chunks).replace('\n', '<br>')

st.html('<div class="brand"><span class="brand-icon">tq.</span><span>TechScript <b>QA</b></span></div>')

stage_index = {"input": 0, "review": 1, "result": 2}[s.stage]
st.html('<nav class="steps" aria-label="Tiến trình">' + ''.join(f'<span class="step {"current" if i == stage_index else "done" if i < stage_index else ""}"><b>0{i+1}</b> {label}</span>' for i, label in enumerate(["Nhập kịch bản", "Duyệt gợi ý", "Bản hoàn chỉnh"])) + '</nav>')

if s.stage == "input":
    st.html('<div class="eyebrow">KHÔNG GIAN BIÊN TẬP KỊCH BẢN</div><h1>Viết đúng ý - Nói tự nhiên hơn</h1><p class="lede">Rà soát cách diễn đạt trước buổi demo, training hoặc quay video.<br>Bạn quyết định từng thay đổi. Thuật ngữ kỹ thuật không tự ý bị sửa.</p>')
    main, aside = st.columns([1.9, 1], gap="large")
    with main:
        with st.container(border=True):
            st.subheader("Kịch bản của bạn")
            st.selectbox("Bắt đầu từ một tình huống", list(SAMPLES), key="sample", on_change=load_sample)
            st.selectbox("Bạn sẽ trình bày cho ai?", ["Đồng nghiệp ít chuyên môn kỹ thuật", "Nhóm Dev / BA / PM", "Học viên mới bắt đầu"], key="audience", on_change=invalidate)
            st.text_area("Nội dung cần rà soát", key="source", height=235, max_chars=12000, on_change=invalidate, placeholder="Dán lời bạn định nói, không chỉ tiêu đề slide…")
            st.caption(f"{len(s.source):,} / 12.000 ký tự")
            if st.button("Rà soát kịch bản", type="primary", use_container_width=True):
                try:
                    if s.engine_mode == "AI Thật (GPT-4o-mini)":
                        with st.spinner("Đang gửi kịch bản đến mô hình AI"):
                            s.findings, s.covered = analyze_script_ai(s.source)
                    else:
                        with st.spinner("Đang đối chiếu với các tình huống mô phỏng…"):
                            s.findings, s.covered = analyze(s.source)
                    s.decisions, s.events = {}, []
                    s.run_hash = fingerprint(s.source, s.audience)
                    s.run_count += 1
                    s.stage = "review"
                    st.rerun()
                except (ValueError, RuntimeError) as error:
                    st.error(str(error))
    with aside:
        st.html('<div class="side-note"><div class="eyebrow">MỘT GỢI Ý, MỘT QUYẾT ĐỊNH</div><h3>Ít chỉnh sửa hơn.<br>Rõ ý hơn.</h3><div class="sample-after">áp dụng một phương pháp</div><p>Chỉ thay cụm cần thiết. Phần còn lại của kịch bản được giữ nguyên.</p><hr><div class="note-row"><b>01</b><span>Nhìn đúng đoạn cần xem lại</span></div><div class="note-row"><b>02</b><span>Chấp nhận, tự sửa hoặc giữ nguyên</span></div><div class="note-row"><b>03</b><span>Tải bản cuối cùng và lịch sử duyệt</span></div></div>')
else:
    if s.run_hash != fingerprint(s.source, s.audience):
        invalidate()
        st.rerun()
    findings = s.findings
    reviewed = len(s.decisions)
    if s.stage == "review":
        st.html('<div class="eyebrow">BẠN LÀ NGƯỜI BIÊN TẬP CUỐI CÙNG</div><h1>Đọc lại - Chọn cách nói</h1>')
        if not s.covered:
            st.warning("Đây là nội dung ngoài mẫu demo. AI rà soát toàn bộ văn bản và trích xuất các span lỗi cần tối ưu.")
        if s.engine_mode == "AI Thật (GPT-4o-mini)":
            st.caption(f"Người nghe: {s.audience} · {reviewed}/{len(findings)} gợi ý đã duyệt · Phân tích bởi GPT-4o-mini.")
        else:
            st.caption(f"Người nghe: {s.audience} · {reviewed}/{len(findings)} gợi ý đã duyệt · API và JSON được giữ nguyên trong mẫu demo.")
        st.progress(reviewed / len(findings) if findings else 1.0)
        if findings:
            main, aside = st.columns([1.35, 1], gap="large")
            with aside:
                with st.container(border=True):
                    st.subheader("Gợi ý biên tập")
                    def finding_label(index):
                        f = findings[index]
                        return f"{index + 1}. {f.original}"
                    labels = [finding_label(i) for i in range(len(findings))]
                    pick_key = f"pick_{s.run_count}"
                    queued_key = f"queued_pick_{s.run_count}"
                    if queued_key in s:
                        s[pick_key] = s.pop(queued_key)
                    idx = st.selectbox("Chọn đoạn cần duyệt", range(len(findings)), format_func=labels.__getitem__, key=pick_key)
                    item = findings[idx]
                    st.html(f'<span class="tag {"caution" if item.uncertain else ""}">{escape(item.category)}</span>')
                    st.write(item.reason)
                    st.caption("Đoạn gốc")
                    st.markdown(f"> {item.original}")
                    if item.uncertain:
                        st.warning("Chưa có đề xuất tự động an toàn. Bạn có thể tự nhập bản thay thế hoặc chọn Giữ nguyên.")
                    edit_key = f"edit_{s.run_count}_{item.id}"
                    prior_decision = s.decisions.get(item.id, {})
                    if edit_key not in s or (
                        not prior_decision and item.suggestion.strip() and not str(s[edit_key]).strip()
                    ):
                        s[edit_key] = prior_decision.get("replacement", item.suggestion)
                    if item.suggestion.strip():
                        st.caption("Gợi ý AI đã được điền sẵn bên dưới; bạn có thể sửa trước khi áp dụng.")
                    replacement = st.text_area("Cách nói thay thế — bạn có thể chỉnh sửa", key=edit_key, height=100, placeholder="Nhập cách diễn đạt đã được bạn xác nhận…")
                    a, b = st.columns(2)
                    with a:
                        if st.button("Áp dụng gợi ý" if not item.uncertain else "Áp dụng bản tự sửa", type="primary", use_container_width=True):
                            if not replacement.strip():
                                st.error("Hãy nhập nội dung thay thế hoặc chọn Giữ nguyên.")
                            else:
                                event(item, "accept", replacement.strip())
                                queue_next_pending(findings, idx)
                                st.rerun()
                    with b:
                        if st.button("Giữ nguyên", use_container_width=True):
                            event(item, "keep")
                            queue_next_pending(findings, idx)
                            st.rerun()
                    if item.id in s.decisions:
                        action = s.decisions[item.id]["action"]
                        st.success("Đã áp dụng bản sửa." if action == "accept" else "Đã giữ nguyên đoạn gốc.")
                        if st.button("Hoàn tác quyết định"):
                            del s.decisions[item.id]
                            s.events.append({"at": datetime.now(timezone.utc).isoformat(), "finding_id": item.id, "action": "undo"})
                            st.rerun()
                    st.caption("Chỉnh ô nhập chưa làm thay đổi bản cuối. Hãy bấm Áp dụng để lưu quyết định.")
            with main:
                with st.container(border=True):
                    st.subheader("Bản gốc có đánh dấu")
                    clicked = clickable_script(
                        key=f"clickable_script_{s.run_count}",
                        data={"html": clickable_document_html(s.source, findings, item.id)},
                        height=REVIEW_SCRIPT_HEIGHT,
                        on_selected_change=lambda: None,
                    )
                    selected = clicked.selected
                    if isinstance(selected, str) and "|" in selected and selected != s.get("last_finding_click"):
                        selected_id, _ = selected.rsplit("|", 1)
                        s.last_finding_click = selected
                        clicked_index = next(
                            (index for index, finding in enumerate(findings) if finding.id == selected_id),
                            None,
                        )
                        if clicked_index is not None and clicked_index != idx:
                            s[f"queued_pick_{s.run_count}"] = clicked_index
                            st.rerun()
                    st.html('<div class="legend"><span>Vàng · chờ duyệt</span><span>Xanh · đã áp dụng</span><span>Xám · giữ nguyên</span></div>')
                    st.caption("Cuộn trong khung để đọc văn bản dài. Nhấn vào đoạn được tô để mở đúng gợi ý.")
        else:
            if s.covered:
                st.success("Mẫu minh họa này không có gợi ý sửa trong bộ mô phỏng.")
            else:
                st.info("Không tìm thấy cụm nào trong bộ mô phỏng. Bạn vẫn có thể xuất bản gốc, nhưng cần tự rà soát nội dung.")
            st.html(document_html(s.source, []))
        st.divider()
        a, b = st.columns([1, 1])
        with a:
            if st.button("← Sửa kịch bản đầu vào"):
                invalidate()
                st.rerun()
        with b:
            if st.button("Xem bản hoàn chỉnh →", type="primary", disabled=reviewed != len(findings), use_container_width=True):
                s.stage = "result"
                st.rerun()
            if reviewed != len(findings):
                st.caption(f"Còn {len(findings) - reviewed} gợi ý cần bạn quyết định.")
    else:
        final = render_final(s.source, findings, s.decisions)
        applied = sum(d["action"] == "accept" for d in s.decisions.values())
        st.html('<div class="eyebrow">BẢN HOÀN CHỈNH · ĐÃ ĐƯỢC BẠN DUYỆT</div><h1>Sẵn sàng cho lần đọc thử</h1>')
        st.caption(f"{applied} cụm đã sửa · {len(findings) - applied} cụm giữ nguyên · Không thay đổi phần ngoài các cụm đã duyệt.")
        main, aside = st.columns([1.8, 1], gap="large")
        with main:
            st.html('<div class="final-document"><div class="eyebrow">KỊCH BẢN SAU BIÊN TẬP</div>' + document_html(final, []) + '</div>')
        with aside:
            with st.container(border=True):
                st.subheader("Mang vào buổi trình bày")
                st.write("Đọc thành lời một lượt và kiểm tra lại ý nghĩa kỹ thuật trước khi sử dụng.")
                st.download_button("Tải kịch bản · TXT", final, "techscript-final.txt", "text/plain", type="primary", use_container_width=True)
                payload = audit_payload(s.source, s.audience, findings, s.decisions, s.events, s.covered)
                st.download_button("Tải lịch sử duyệt · JSON", json.dumps(payload, ensure_ascii=False, indent=2), "techscript-review.json", "application/json", use_container_width=True)
                st.caption("Tệp lịch sử có bản gốc, bản cuối và các quyết định của bạn. Kiểm tra thông tin nội bộ trước khi chia sẻ.")
            if not s.covered:
                st.warning("Ngoài mẫu demo: bản này chỉ được đối chiếu một phần bằng bộ mô phỏng, không phải kết quả kiểm định AI.")
        with st.expander("Đối chiếu các quyết định"):
            if findings:
                st.dataframe([{"Đoạn gốc": f.original, "Quyết định": "Áp dụng" if s.decisions[f.id]["action"] == "accept" else "Giữ nguyên", "Nội dung cuối": s.decisions[f.id]["replacement"] if s.decisions[f.id]["action"] == "accept" else f.original} for f in findings], hide_index=True, use_container_width=True)
            else:
                st.write("Không có thay đổi. Bản xuất giống bản gốc.")
        a, b = st.columns(2)
        with a:
            if st.button("← Quay lại duyệt gợi ý"):
                s.stage = "review"
                st.rerun()
        with b:
            if st.button("Biên tập kịch bản khác", use_container_width=True):
                invalidate()
                st.rerun()

st.html('<footer>TechScript QA <span>Người viết quyết định. Công cụ chỉ gợi ý.</span></footer>')
