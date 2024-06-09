import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("a", "value", [], {"href": "dummy.url"})
        expected = ' href="dummy.url"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_2(self):
        node = HTMLNode(
            "a", "value", [], {"href": "https://google.com", "target": "_blank"}
        )
        expected = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_3(self):
        node = HTMLNode("a", "value", [], {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_eq(self):
        node = HTMLNode("a", "Click this link", [], {"href": "https://google.com"})
        node2 = HTMLNode("a", "Click this link", [], {"href": "https://google.com"})
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
