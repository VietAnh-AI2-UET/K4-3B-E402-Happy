import os
os.environ["STREAMLIT_TESTING"] = "1"
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from core import SAMPLES

APP = str(Path(__file__).with_name("app.py"))

def button(app, label):
    return next(b for b in app.button if b.label == label)

class UIFlowTests(unittest.TestCase):
    def start(self):
        app = AppTest.from_file(APP, default_timeout=20).run()
        self.assertEqual(len(app.exception), 0)
        return app

    def test_happy_path_edit_keep_undo_export(self):
        app = self.start()
        button(app, "Rà soát kịch bản").click().run()
        self.assertTrue(button(app, "Xem bản hoàn chỉnh →").disabled)
        app.text_area[0].input("áp dụng phương pháp phù hợp").run()
        button(app, "Áp dụng gợi ý").click().run()
        button(app, "Hoàn tác quyết định").click().run()
        self.assertEqual(len(app.session_state["decisions"]), 0)
        button(app, "Áp dụng gợi ý").click().run()
        for idx in range(1, 4):
            app.selectbox[0].select_index(idx).run()
            button(app, "Giữ nguyên").click().run()
        self.assertFalse(button(app, "Xem bản hoàn chỉnh →").disabled)
        button(app, "Xem bản hoàn chỉnh →").click().run()
        self.assertEqual(app.session_state["stage"], "result")
        self.assertEqual(len(app.get("download_button")), 2)
        self.assertEqual(app.session_state["source"], SAMPLES["Demo tính năng · Dev / BA"])
        self.assertEqual(len(app.exception), 0)
        button(app, "← Quay lại duyệt gợi ý").click().run()
        self.assertEqual(len(app.session_state["decisions"]), 4)
        button(app, "← Sửa kịch bản đầu vào").click().run()
        self.assertEqual(app.session_state["decisions"], {})

    def test_uncertain_nondefault_source_persists(self):
        app = self.start()
        app.selectbox[0].select("Thuật ngữ cần giữ · PM").run()
        button(app, "Rà soát kịch bản").click().run()
        button(app, "Áp dụng bản tự sửa").click().run()
        self.assertEqual(len(app.error), 1)
        button(app, "Giữ nguyên").click().run()
        button(app, "Xem bản hoàn chỉnh →").click().run()
        self.assertEqual(app.session_state["stage"], "result")
        self.assertEqual(app.session_state["source"], SAMPLES["Thuật ngữ cần giữ · PM"])
        self.assertEqual(len(app.exception), 0)

    def test_empty_and_unknown_input(self):
        app = self.start()
        app.selectbox[0].select("Kịch bản của bạn").run()
        button(app, "Rà soát kịch bản").click().run()
        self.assertEqual(len(app.error), 1)
        app.text_area[0].input("Một đoạn chưa có trong bộ mô phỏng.").run()
        button(app, "Rà soát kịch bản").click().run()
        self.assertFalse(app.session_state["covered"])
        self.assertGreater(len(app.warning), 0)
        button(app, "Xem bản hoàn chỉnh →").click().run()
        self.assertEqual(app.session_state["source"], "Một đoạn chưa có trong bộ mô phỏng.")
        self.assertEqual(len(app.exception), 0)

if __name__ == "__main__":
    unittest.main()
