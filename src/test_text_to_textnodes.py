import unittest

from markdown_operations import TextNode, text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_all_cases(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block","code"),
            TextNode(" and an ","text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_only_text(self):
        text = "This is just normal text. This should only return one TextNode object."
        expected = [TextNode("This is just normal text. This should only return one TextNode object.", "text")]
        self.assertEqual(text_to_textnodes(text), expected)
