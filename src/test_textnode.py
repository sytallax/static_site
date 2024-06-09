import unittest

from leafnode import LeafNode
from markdown_operations import text_node_to_html_node
from textnode import TextNode, TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertEqual(node, node2)

    def test_no_none_url_eq(self):
        node = TextNode("This is a text node", TextNodeType.BOLD, "https://fake.url")
        node2 = TextNode("This is a text node", TextNodeType.BOLD, "https://fake.url")
        self.assertEqual(node, node2)

    def test_when_text_different_objects_not_equal(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This isn't a text node", TextNodeType.BOLD)
        self.assertNotEqual(node, node2)

    def test_when_types_different_object_not_equal(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_when_url_different_object_not_equal(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.BOLD, "https://fake.url")
        self.assertNotEqual(node, node2)

    def test_when_no_none_url_different_object_not_equal(self):
        node = TextNode("This is a text node", TextNodeType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextNodeType.BOLD, "https://fake.url")
        self.assertNotEqual(node, node2)


class TestTextModeToHtmlNode(unittest.TestCase):
    def test_text_conversion(self):
        node = TextNode("This is normal text", TextNodeType.TEXT)
        expected = LeafNode(value="This is normal text")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_bold_conversion(self):
        node = TextNode("This is bold text", TextNodeType.BOLD)
        expected = LeafNode(tag="b", value="This is bold text")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_link_conversion(self):
        node = TextNode("Click this link!", TextNodeType.LINK, "https://google.com")
        expected = LeafNode("Click this link!", "a", {"href": "https://google.com"})
        self.assertEqual(text_node_to_html_node(node), expected)


if __name__ == "__main__":
    unittest.main()
