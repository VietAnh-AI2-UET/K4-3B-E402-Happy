from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import streamlit as st
from core import SAMPLES, analyze, fingerprint, render_final, audit_payload

st.set_page_config(page_title="TechScript QA · Biên tập để nói", page_icon="✳", layout="wide", initial_sidebar_state="collapsed")
st.html(f"<style>{Path(__file__).with_name('styles.css').read_text(encoding='utf-8')}</style>")
s = st.session_state
for key, value in {"stage": "input", "source": SAMPLES["Demo tính năng · Dev / BA"], "audience": "Đồng nghiệp ít chuyên môn kỹ thuật", "findings": [], "decisions": {}, "events": [], "covered": False, "run_hash": "", "run_count": 0}.items():
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

left, right = st.columns([3, 2])
with left:
    st.html('<div class="brand"><span class="brand-icon">tq.</span><span>TechScript <b>QA</b></span></div>')
with right:
    st.html('<div class="mode"><span class="dot"></span> CP2 · Mô phỏng, chưa kết nối AI</div>')

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
            st.caption(f"{len(s.source):,} / 12.000 ký tự · Chỉ xử lý trong phiên hiện tại, không gọi dịch vụ AI.")
            if st.button("Rà soát kịch bản", type="primary", use_container_width=True):
                try:
                    with st.spinner("Đang đối chiếu với các tình huống mô phỏng…"):
                        s.findings, s.covered = analyze(s.source)
                        s.decisions, s.events = {}, []
                        s.run_hash = fingerprint(s.source, s.audience)
                        s.run_count += 1
                        s.stage = "review"
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    with aside:
        st.html('<div class="side-note"><div class="eyebrow">MỘT GỢI Ý, MỘT QUYẾT ĐỊNH</div><h3>Ít chỉnh sửa hơn.<br>Rõ ý hơn.</h3><p class="sample-before">implement một methodology</p><div class="sample-after">áp dụng một phương pháp</div><p>Chỉ thay cụm cần thiết. Phần còn lại của kịch bản được giữ nguyên.</p><hr><div class="note-row"><b>01</b><span>Nhìn đúng đoạn cần xem lại</span></div><div class="note-row"><b>02</b><span>Chấp nhận, tự sửa hoặc giữ nguyên</span></div><div class="note-row"><b>03</b><span>Tải bản cuối cùng và lịch sử duyệt</span></div></div>')
        st.caption("Phạm vi CP2: cách nói chưa tự nhiên và pha Anh–Việt. Chưa kiểm chứng tính đúng đắn kỹ thuật hay chất lượng của toàn bộ văn bản.")
else:
    if s.run_hash != fingerprint(s.source, s.audience):
        invalidate()
        st.rerun()
    findings = s.findings
    reviewed = len(s.decisions)
    if s.stage == "review":
        st.html('<div class="eyebrow">BẠN LÀ NGƯỜI BIÊN TẬP CUỐI CÙNG</div><h1>Đọc lại - Chọn cách nói</h1>')
        if not s.covered:
            st.warning("Đây là nội dung ngoài mẫu demo. Chỉ các cụm khớp chính xác với bộ mô phỏng được đánh dấu; phần còn lại chưa được đánh giá. Không có gợi ý không có nghĩa là không có lỗi.")
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
                    idx = st.selectbox("Chọn đoạn cần duyệt", range(len(findings)), format_func=labels.__getitem__, key=f"pick_{s.run_count}")
                    item = findings[idx]
                    st.html(f'<span class="tag {"caution" if item.uncertain else ""}">{escape(item.category)}</span>')
                    st.write(item.reason)
                    st.caption("Đoạn gốc")
                    st.markdown(f"> {item.original}")
                    if item.uncertain:
                        st.warning("Chưa có đề xuất an toàn. Mặc định giữ nguyên thuật ngữ; chỉ thay khi bạn đã xác nhận ý nghĩa.")
                    edit_key = f"edit_{s.run_count}_{item.id}"
                    if edit_key not in s:
                        s[edit_key] = s.decisions.get(item.id, {}).get("replacement", item.suggestion)
                    replacement = st.text_area("Cách nói thay thế — bạn có thể chỉnh sửa", key=edit_key, height=100, placeholder="Nhập cách diễn đạt đã được bạn xác nhận…")
                    a, b = st.columns(2)
                    with a:
                        if st.button("Áp dụng gợi ý" if not item.uncertain else "Áp dụng bản tự sửa", type="primary", use_container_width=True):
                            if not replacement.strip():
                                st.error("Hãy nhập nội dung thay thế hoặc chọn Giữ nguyên.")
                            else:
                                event(item, "accept", replacement.strip())
                                st.rerun()
                    with b:
                        if st.button("Giữ nguyên", use_container_width=True):
                            event(item, "keep")
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
                st.subheader("Bản gốc có đánh dấu")
                st.html(document_html(s.source, findings, item.id))
                st.html('<div class="legend"><span>Vàng · chờ duyệt</span><span>Xanh · đã áp dụng</span><span>Xám · giữ nguyên</span></div>')
                st.caption("Đang xem bản gốc để đối chiếu. Bản đã sửa nằm ở bước 03.")
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
