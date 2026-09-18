import os
os.environ["STREAMLIT_TESTING"] = "1"
import unittest

from agent.model import add_uncovered_english_sentences
from core import Finding


class EnglishCoverageTests(unittest.TestCase):
    def test_adds_only_the_uncovered_adjacent_english_sentence(self):
        source = "That's pretty much it for this demo. Thank you everyone, and I'm happy to take any questions."
        first_sentence = "That's pretty much it for this demo."
        findings = [Finding(
            id="0_0",
            start=0,
            end=len(first_sentence),
            original=first_sentence,
            suggestion="Đó là phần trình diễn hôm nay.",
            category="Sượng / Dịch trực tiếp",
            reason="Câu tiếng Anh.",
            uncertain=False,
        )]

        covered = add_uncovered_english_sentences(source, findings)

        self.assertEqual(len(covered), 2)
        self.assertEqual(covered[1].original, "Thank you everyone, and I'm happy to take any questions.")
        self.assertTrue(covered[1].uncertain)
        self.assertEqual(covered[1].suggestion, "")


if __name__ == "__main__":
    unittest.main()
