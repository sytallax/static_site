import unittest

from textnode import TextNode
from markdown_operations import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_two_links(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.maxDiff = None
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_one_link(self):
        node = TextNode("This is text with a [link](https://fake.image/image.png).", "text")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://fake.image/image.png"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_expected_when_image_not_link(self):
        node = TextNode("This is an  ![image](https://google.com/photo.png), and it shouln't be split by this function.", "text")
        expected = TextNode("This is an  ![image](https://google.com/photo.png), and it shouln't be split by this function.", "text")
        self.assertEqual(split_nodes_link([node]), [expected])

    def test_expected_when_just_text(self):
        node = TextNode("This is just regular text, please keep me whole!", "text")
        expected = TextNode("This is just regular text, please keep me whole!", "text")
        self.assertEqual(split_nodes_link([node]), [expected])

    def test_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        ),
            TextNode("This node also contains [this](https://google.com) link.", "text")
        ]
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode("This node also contains ", "text"),
            TextNode("this", "link", "https://google.com"),
            TextNode(" link.", "text")
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

if __name__ == "__main__":
    unittest.main()
