import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_1(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_2(self):
        node = LeafNode(value="This is a paragraph of text.")
        expected = "This is a paragraph of text."
        self.assertEqual(node.to_html(), expected)

    def test_to_html_3(self):
        node = LeafNode(
            tag="a",
            value="Click me!",
            props={"href": "https://google.com"},
        )
        expected = '<a href="https://google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)
