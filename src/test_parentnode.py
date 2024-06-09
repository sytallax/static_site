import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_1(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(value="Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_2(self):
        node = ParentNode(
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(value="Normal text"),
            ],
        )
        expected_error = "ParentNode has no tag"
        try:
            node.to_html()
        except ValueError as e:
            self.assertEqual(f"{e}", expected_error)
        else:
            raise AssertionError("ValueError was not raised")

    def test_to_html_3(self):
        node = ParentNode(tag="p", children=[])
        expected_error = "ParentNode has no children"
        try:
            node.to_html()
        except ValueError as e:
            self.assertEqual(f"{e}", expected_error)
        else:
            raise AssertionError("ValueError was not raised")

    def test_to_html_4(self):
        node = ParentNode(tag="p", children=[LeafNode(value="This is normal text")])
        expected = "<p>This is normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_5(self):
        node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="Bold text in inner"),
                        LeafNode(value="Normal text in inner"),
                    ],
                ),
                LeafNode(tag="i", value="Italic text in outer"),
            ],
        )
        expected = "<p><p><b>Bold text in inner</b>Normal text in inner</p><i>Italic text in outer</i></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_6(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(value="This is normal text with "),
                LeafNode(tag="a", value="links", props={"href": "https://google.com"}),
            ],
        )
        expected = (
            '<p>This is normal text with <a href="https://google.com">links</a></p>'
        )
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
