import unittest

from markdown_operations import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_expected_1(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_expected_2(self):
        markdown = "This is **bolded** paragraph. \n\n This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items "
        expected = [
            "This is **bolded** paragraph.",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_expected_3(self):
        markdown = " This is just one paragraph "
        expected = ["This is just one paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

