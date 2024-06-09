import unittest

from htmlnode import HTMLNode
from markdown_operations import split_nodes_delimiter
from textnode import TextNode, TextNodeType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a **bolded** word", TextNodeType.TEXT)
        expected = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("bolded", TextNodeType.BOLD),
            TextNode(" word", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected)

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is text with a `code block` word", TextNodeType.TEXT)
        expected = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("code block", TextNodeType.CODE),
            TextNode(" word", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), expected)

    def test_split_nodes_delimiter_3(self):
        node = HTMLNode("p", "This is a paragraph in HTML")
        expected = [HTMLNode("p", "This is a paragraph in HTML")]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected)

    def test_split_nodes_delimiter_4(self):
        node = TextNode("This code shouldn't be split", TextNodeType.TEXT)
        expected = [TextNode("This code shouldn't be split", TextNodeType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected)

    def test_split_nodes_delimiter_5(self):
        node = TextNode("This is **invalid bold text", TextNodeType.TEXT)
        expected = "Invalid Markdown syntax. No closing delimiter."
        try:
            split_nodes_delimiter([node], "**", "bold")
        except Exception as e:
            self.assertEqual(f"{e}", expected)
        else:
            raise AssertionError("Expected exception wasn't raised.")

    def test_split_nodes_delimiter_6(self):
        nodes = [
            TextNode("This is **bold text**", TextNodeType.TEXT),
            TextNode(" combined with `code` text", TextNodeType.TEXT),
        ]
        expected = [
            TextNode("This is ", TextNodeType.TEXT),
            TextNode("bold text", TextNodeType.BOLD),
            TextNode(" combined with `code` text", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", "bold"), expected)

    def test_split_nodes_delimiter_7(self):
        nodes = [
            TextNode("This is **bold text**", TextNodeType.TEXT),
            TextNode(" with **more** bold text", TextNodeType.TEXT),
        ]
        expected = [
            TextNode("This is ", TextNodeType.TEXT),
            TextNode("bold text", TextNodeType.BOLD),
            TextNode(" with ", TextNodeType.TEXT),
            TextNode("more", TextNodeType.BOLD),
            TextNode(" bold text", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", "bold"), expected)

if __name__ == "__main__":
    unittest.main()
