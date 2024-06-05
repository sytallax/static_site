import unittest

from markdown_operations import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_normal_paragraph(self):
        block = "This is normal text"
        expected = "paragraph"
        self.assertEqual(block_to_block_type(block), expected)

    def test_heading(self):
        block = "# This is a header"
        expected = "heading"
        self.assertEqual(block_to_block_type(block), expected)

    def test_three_heading(self):
        block = "### This is a header"
        expected = "heading"
        self.assertEqual(block_to_block_type(block), expected)

    def test_invalid_heading(self):
        block = "####### This has more than 6, so its invalid"
        expected = "paragraph"
        self.assertEqual(block_to_block_type(block), expected)

    def test_code(self):
        block = "```\nThis should be code\n```"
        expected = "code"
        self.assertEqual(block_to_block_type(block), expected)

    def test_ul(self):
        block = "* This is item one\n* This is item two\n* This is item three"
        expected = "unordered_list"
        self.assertEqual(block_to_block_type(block), expected)

    def test_ol(self):
        block = "1. This is item one\n2. This is item two\n3. This is item three"
        expected = "ordered_list"
        self.assertEqual(block_to_block_type(block), expected)
