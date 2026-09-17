import unittest
from core import SAMPLES, analyze, render_final, audit_payload, fingerprint

class ReviewTests(unittest.TestCase):
    def test_demo_and_minimal_edits(self):
        source = SAMPLES["Demo tính năng · Dev / BA"]
        findings, covered = analyze(source)
        self.assertTrue(covered)
        self.assertEqual(len(findings), 4)
        decisions = {f.id: {"action": "accept", "replacement": f.suggestion} for f in findings}
        result = render_final(source, findings, decisions)
        expected = source
        for f in findings:
            expected = expected.replace(f.original, f.suggestion, 1)
        self.assertEqual(result, expected)
        self.assertIn("API trả về dữ liệu dạng JSON.", result)

    def test_repeated_spans_are_independent(self):
        source = "improve kết quả; improve kết quả"
        findings, _ = analyze(source)
        decisions = {findings[0].id: {"action": "accept", "replacement": "cải thiện kết quả"}, findings[1].id: {"action": "keep", "replacement": ""}}
        self.assertEqual(render_final(source, findings, decisions), "cải thiện kết quả; improve kết quả")

    def test_uncertain_requires_human(self):
        source = SAMPLES["Thuật ngữ cần giữ · PM"]
        findings, _ = analyze(source)
        self.assertEqual(len(findings), 1)
        self.assertTrue(findings[0].uncertain)
        self.assertEqual(findings[0].suggestion, "")
        with self.assertRaises(ValueError):
            render_final(source, findings, {})
        decisions = {findings[0].id: {"action": "keep", "replacement": ""}}
        self.assertEqual(render_final(source, findings, decisions), source)

    def test_empty_replacement_rejected(self):
        findings, _ = analyze("improve kết quả")
        with self.assertRaises(ValueError):
            render_final("improve kết quả", findings, {findings[0].id: {"action": "accept", "replacement": " "}})

    def test_coverage_is_not_quality_claim(self):
        self.assertEqual(analyze("Văn bản bất kỳ chưa từng gặp."), ([], False))
        self.assertEqual(analyze(SAMPLES["Mẫu đã rõ ràng"]), ([], True))

    def test_invalid_source(self):
        for source in ["  ", "a" * 12001]:
            with self.assertRaises(ValueError):
                analyze(source)

    def test_audit_and_source_hash(self):
        source = "improve kết quả"
        findings, covered = analyze(source)
        decisions = {findings[0].id: {"action": "accept", "replacement": "nâng chất lượng kết quả"}}
        payload = audit_payload(source, "BA", findings, decisions, [{"action": "accept"}], covered)
        self.assertEqual(payload["original"], source)
        self.assertEqual(payload["final"], "nâng chất lượng kết quả")
        self.assertEqual(len(payload["events"]), 1)
        self.assertNotEqual(fingerprint(source, "BA"), fingerprint(source + ".", "BA"))
        self.assertNotEqual(fingerprint(source, "BA"), fingerprint(source, "PM"))

if __name__ == "__main__":
    unittest.main()
