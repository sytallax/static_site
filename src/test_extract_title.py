import unittest
from markdown_operations import extract_title

class TestExtractTitle(unittest.TestCase):
    def text_expected_1(self):
        markdown = "# My Website\n\nThis is my website! Here you will find:\n\n* Nothing\n* Because this is fake"
        expected = "My Website"
        self.assertEqual(extract_title(markdown), expected)
    def test_expected_2(self):
        markdown = "# This is just a title"
        expected = "This is just a title"
        self.assertEqual(extract_title(markdown), expected)

    def test_expected_3(self):
        markdown = "This document doesn't have a title. This is a big nono."
        expected = "Markdown document has no title"
        try:
            extract_title(markdown)
        except Exception as e:
            self.assertEqual(f"{e}", expected)
        else:
            raise AssertionError("Expected exception not raised")
