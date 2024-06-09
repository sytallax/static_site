import unittest

from markdown_operations import LeafNode, ParentNode, _ordered_list_to_html_node


class TestOrderedListToHTMLNode(unittest.TestCase):
    def test_expected_1(self):
        block = "1. This is an ordered list with one item"
        expected = ParentNode(
            [LeafNode("This is an ordered list with one item", "li")], "ol"
        )
        self.assertEqual(_ordered_list_to_html_node(block), expected)

    def test_expected_2(self):
        block = "1. This is an ordered list\n2. With multiple items"
        expected = ParentNode(
            [
                LeafNode("This is an ordered list", "li"),
                LeafNode("With multiple items", "li"),
            ],
            "ol",
        )
        self.assertEqual(_ordered_list_to_html_node(block), expected)

    def test_inline_1(self):
        block = "1. This list entry has a **bold** word\n2. This one is normal"
        expected = ParentNode(
            [
                ParentNode([LeafNode("This list entry has a "), LeafNode("bold", "b"), LeafNode(" word")], "li"),
                LeafNode("This one is normal", "li"),
            ],
            "ol"
        )
        self.assertEqual(_ordered_list_to_html_node(block), expected)

if __name__ == "__main__":
    unittest.main()
