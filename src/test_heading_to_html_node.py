import unittest

from markdown_operations import LeafNode, ParentNode, _heading_to_html_node


class TestHeadingToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "# This is a heading"
        expected = LeafNode("This is a heading", "h1")
        self.assertEqual(_heading_to_html_node(block), expected)

    def test_expected_2(self):
        block = "## This is a 2nd level heading"
        expected = LeafNode("This is a 2nd level heading", "h2")
        self.assertEqual(_heading_to_html_node(block), expected)

    def test_inline_1(self):
        block = "# This is a heading with **bold** text"
        expected = ParentNode(
            [
                LeafNode("This is a heading with "),
                LeafNode("bold", "b"),
                LeafNode(" text"),
            ],
            "h1",
        )
        self.assertEqual(_heading_to_html_node(block), expected)

    def test_inline_2(self):
        block = "## This is a heading with *italic* text"
        expected = ParentNode(
            [
                LeafNode("This is a heading with "),
                LeafNode("italic", "i"),
                LeafNode(" text"),
            ],
            "h2",
        )
        self.assertEqual(_heading_to_html_node(block), expected)
