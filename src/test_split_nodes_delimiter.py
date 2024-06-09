import unittest

from htmlnode import HTMLNode
from markdown_operations import split_nodes_delimiter
from textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a **bolded** word", "text")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected)

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is text with a `code block` word", "text")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), expected)

    def test_split_nodes_delimiter_3(self):
        node = HTMLNode("p", "This is a paragraph in HTML")
        expected = [HTMLNode("p", "This is a paragraph in HTML")]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected)

    def test_split_nodes_delimiter_4(self):
        node = TextNode("This code shouldn't be split", "text")
        expected = [TextNode("This code shouldn't be split", "text")]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected)

    def test_split_nodes_delimiter_5(self):
        node = TextNode("This is **invalid bold text", "text")
        expected = "Invalid Markdown syntax. No closing delimiter."
        try:
            split_nodes_delimiter([node], "**", "bold")
        except Exception as e:
            self.assertEqual(f"{e}", expected)
        else:
            raise AssertionError("Expected exception wasn't raised.")

    def test_split_nodes_delimiter_6(self):
        nodes = [
            TextNode("This is **bold text**", "text"),
            TextNode(" combined with `code` text", "text"),
        ]
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold text", "bold"),
            TextNode(" combined with `code` text", "text"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", "bold"), expected)

    def test_split_nodes_delimiter_7(self):
        nodes = [
            TextNode("This is **bold text**", "text"),
            TextNode(" with **more** bold text", "text"),
        ]
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold text", "bold"),
            TextNode(" with ", "text"),
            TextNode("more", "bold"),
            TextNode(" bold text", "text"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", "bold"), expected)

if __name__ == "__main__":
    unittest.main()
