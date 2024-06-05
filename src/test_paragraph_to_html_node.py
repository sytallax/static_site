import unittest

from leafnode import LeafNode
from markdown_operations import ParentNode, _paragraph_to_html_node


class TestParagraphToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "This is a normal paragraph"
        expected = LeafNode("This is a normal paragraph", "p")
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_expected_2(self):
        block = "This is a normal paragraph\non two lines"
        expected = LeafNode("This is a normal paragraph on two lines", "p")
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_inline_1(self):
        block = "This is a normal paragraph with **bold** text."
        expected = ParentNode(
            [
                LeafNode("This is a normal paragraph with "),
                LeafNode("bold", "b"),
                LeafNode(" text."),
            ],
            "p",
        )
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_inline_link(self):
        block = "This is a paragraph with a [link](https://google.com) to google."
        expected = ParentNode(
            [
                LeafNode("This is a paragraph with a "),
                LeafNode("link", "a", {"href": "https://google.com"}),
                LeafNode(" to google."),
            ],
            "p",
        )
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_inline_image(self):
        block = "This is a paragraph with an ![image](https://google.com) of google."
        expected = ParentNode(
            [
                LeafNode("This is a paragraph with an "),
                LeafNode("", "img", {"src": "https://google.com", "alt": "image"}),
                LeafNode(" of google."),
            ],
            "p",
        )
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_standalone_link(self):
        block = "[This is just one link](https://google.com)"
        expected = LeafNode(
            "This is just one link", "a", {"href": "https://google.com"}
        )
        self.assertEqual(_paragraph_to_html_node(block), expected)

    def test_standalone_image(self):
        block = "![This is just an image](https://google.com)"
        expected = LeafNode(
            "", "img", {"src": "https://google.com", "alt": "This is just an image"}
        )
        self.assertEqual(_paragraph_to_html_node(block), expected)
