import unittest

from markdown_operations import LeafNode, ParentNode, _unordered_list_to_html_node


class TestUnorderedListToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "* This is an unordered list with one item"
        expected = ParentNode(
            [LeafNode("This is an unordered list with one item", "li")], "ul"
        )
        self.assertEqual(_unordered_list_to_html_node(block), expected)

    def test_expected_2(self):
        block = "* This is an unordered_list\n* With multiple items"
        expected = ParentNode(
            [
                LeafNode("This is an unordered_list", "li"),
                LeafNode("With multiple items", "li"),
            ],
            "ul",
        )
        self.assertEqual(_unordered_list_to_html_node(block), expected)

    def test_inline_1(self):
        block = "* This list entry has a **bold** word\n* This one is normal"
        expected = ParentNode(
            [
                ParentNode([LeafNode("This list entry has a "), LeafNode("bold", "b"), LeafNode(" word")], "li"),
                LeafNode("This one is normal", "li"),
            ],
            "ul"
        )
        self.assertEqual(_unordered_list_to_html_node(block), expected)

if __name__ == "__main__":
    unittest.main()
