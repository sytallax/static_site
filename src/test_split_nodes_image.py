import unittest

from textnode import TextNode, TextNodeType
from markdown_operations import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode(
                "image",
                TextNodeType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second image",
                TextNodeType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.maxDiff = None
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://fake.image/image.png).",
            TextNodeType.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://fake.image/image.png"),
            TextNode(".", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_expected_when_link_not_image(self):
        node = TextNode(
            "This is a [link](https://google.com), and it shouln't be split by this function.",
            TextNodeType.TEXT,
        )
        expected = TextNode(
            "This is a [link](https://google.com), and it shouln't be split by this function.",
            TextNodeType.TEXT,
        )
        self.assertEqual(split_nodes_image([node]), [expected])

    def test_expected_when_just_text(self):
        node = TextNode(
            "This is just regular text, please keep me whole!", TextNodeType.TEXT
        )
        expected = TextNode(
            "This is just regular text, please keep me whole!", TextNodeType.TEXT
        )
        self.assertEqual(split_nodes_image([node]), [expected])

    def test_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                TextNodeType.TEXT,
            ),
            TextNode(
                "This node also contains ![this](https://google.com) image.",
                TextNodeType.TEXT,
            ),
        ]
        expected = [
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode(
                "image",
                TextNodeType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second image",
                TextNodeType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode("This node also contains ", TextNodeType.TEXT),
            TextNode("this", TextNodeType.IMAGE, "https://google.com"),
            TextNode(" image.", TextNodeType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)


if __name__ == "__main__":
    unittest.main()
