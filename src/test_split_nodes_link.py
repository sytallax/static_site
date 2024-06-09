import unittest

from textnode import TextNode, TextNodeType
from markdown_operations import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_two_links(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        expected = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode(
                "link",
                TextNodeType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second link",
                TextNodeType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.maxDiff = None
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_one_link(self):
        node = TextNode("This is text with a [link](https://fake.image/image.png).", TextNodeType.TEXT)
        expected = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://fake.image/image.png"),
            TextNode(".", TextNodeType.TEXT)
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_expected_when_image_not_link(self):
        node = TextNode("This is an  ![image](https://google.com/photo.png), and it shouln't be split by this function.", TextNodeType.TEXT)
        expected = TextNode("This is an  ![image](https://google.com/photo.png), and it shouln't be split by this function.", TextNodeType.TEXT)
        self.assertEqual(split_nodes_link([node]), [expected])

    def test_expected_when_just_text(self):
        node = TextNode("This is just regular text, please keep me whole!", TextNodeType.TEXT)
        expected = TextNode("This is just regular text, please keep me whole!", TextNodeType.TEXT)
        self.assertEqual(split_nodes_link([node]), [expected])

    def test_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.TEXT,
        ),
            TextNode("This node also contains [this](https://google.com) link.", TextNodeType.TEXT)
        ]
        expected = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode(
                "link",
                TextNodeType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second link",
                TextNodeType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode("This node also contains ", TextNodeType.TEXT),
            TextNode("this", TextNodeType.LINK, "https://google.com"),
            TextNode(" link.", TextNodeType.TEXT)
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

if __name__ == "__main__":
    unittest.main()
