import unittest

from markdown_operations import LeafNode, ParentNode, _code_to_html_node


class TestCodeToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "```\nThis is a code block\n```"
        expected = ParentNode([LeafNode("This is a code block", "code")], "pre")
        self.assertEqual(_code_to_html_node(block), expected)

    def test_expected_2(self):
        block = "```This is also a code block```"
        expected = ParentNode([LeafNode("This is also a code block", "code")], "pre")
        self.assertEqual(_code_to_html_node(block), expected)

if __name__ == "__main__":
    unittest.main()
