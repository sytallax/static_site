import unittest

from leafnode import LeafNode
from markdown_operations import markdown_to_html_node
from parentnode import ParentNode


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        markdown = "# My Website\n\nThis is my website! Here you will find:\n\n* Nothing\n* Because this is fake"
        expected = ParentNode(
            [
                LeafNode("My Website", "h1"),
                LeafNode("This is my website! Here you will find:", "p"),
                ParentNode(
                    [LeafNode("Nothing", "li"), LeafNode("Because this is fake", "li")],
                    "ul",
                ),
            ],
            "div",
        )
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_expected_2(self):
        markdown = "## Trying to include everything\n\nThis is an attempt to include everything. For example, some code:\n\n```\nprint(\"Hello, World!\")\n```\n\nHere's a quote:\n\n> Bruh\n\nHere's a list of reasons why this works:\n\n1. I am cool\n2. Profit\n\n And that's that."
        expected = ParentNode(
            [
                LeafNode("Trying to include everything", "h2"),
                LeafNode(
                    "This is an attempt to include everything. For example, some code:",
                    "p",
                ),
                ParentNode([LeafNode('print("Hello, World!")', "code")], "pre"),
                LeafNode("Here's a quote:", "p"),
                LeafNode("Bruh", "blockquote"),
                LeafNode("Here's a list of reasons why this works:", "p"),
                ParentNode(
                    [
                        LeafNode("I am cool", "li"),
                        LeafNode("Profit", "li"),
                    ],
                    "ol",
                ),
                LeafNode("And that's that.", "p"),
            ],
            "div",
        )
        self.assertEqual(markdown_to_html_node(markdown), expected)
