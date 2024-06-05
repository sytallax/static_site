import unittest

from markdown_operations import LeafNode, _quote_to_html_node


class TestQuoteToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "> This is a quote"
        expected = LeafNode("This is a quote", "blockquote")
        self.assertEqual(_quote_to_html_node(block), expected)

    def test_expected_2(self):
        block = "> This will be a quote\n> with multiple lines"
        expected = LeafNode("This will be a quote with multiple lines", "blockquote")
        self.assertEqual(_quote_to_html_node(block), expected)
