import unittest

from markdown_operations import text_to_textnodes
from textnode import TextNode, TextNodeType

class TestTextToTextNodes(unittest.TestCase):
    def test_all_cases(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextNodeType.TEXT),
            TextNode("text", TextNodeType.BOLD),
            TextNode(" with an ", TextNodeType.TEXT),
            TextNode("italic", TextNodeType.ITALIC),
            TextNode(" word and a ", TextNodeType.TEXT),
            TextNode("code block",TextNodeType.CODE),
            TextNode(" and an ",TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_only_text(self):
        text = "This is just normal text. This should only return one TextNode object."
        expected = [TextNode("This is just normal text. This should only return one TextNode object.", TextNodeType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()
