import unittest

from leafnode import LeafNode
from textnode import TextNode

from markdown_operations import text_node_to_html_node


class TestTextModeToHtmlNode(unittest.TestCase):
    def test_text_conversion(self):
        node = TextNode("This is normal text", "text")
        expected = LeafNode(value="This is normal text")
        self.assertEqual(text_node_to_html_node(node), expected)
