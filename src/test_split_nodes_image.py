import unittest

from textnode import TextNode
from markdown_operations import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.maxDiff = None
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_one_image(self):
        node = TextNode("This is text with an ![image](https://fake.image/image.png).", "text")
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://fake.image/image.png"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_expected_when_link_not_image(self):
        node = TextNode("This is a [link](https://google.com), and it shouln't be split by this function.", "text")
        expected = TextNode("This is a [link](https://google.com), and it shouln't be split by this function.", "text")
        self.assertEqual(split_nodes_image([node]), [expected])

    def test_expected_when_just_text(self):
        node = TextNode("This is just regular text, please keep me whole!", "text")
        expected = TextNode("This is just regular text, please keep me whole!", "text")
        self.assertEqual(split_nodes_image([node]), [expected])

    def test_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        ),
            TextNode("This node also contains ![this](https://google.com) image.", "text")
        ]
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode("This node also contains ", "text"),
            TextNode("this", "image", "https://google.com"),
            TextNode(" image.", "text")
        ]
        self.assertEqual(split_nodes_image(nodes), expected)
