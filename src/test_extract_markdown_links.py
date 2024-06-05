import unittest

from markdown_operations import extract_markdown_links


class TestExtractMarkdownFromLinks(unittest.TestCase):
    def test_one_link(self):
        input = "This is text with [a](https://image.com/) link."
        expected = [("a", "https://image.com/")]
        self.assertEqual(extract_markdown_links(input), expected)

    def test_two_links(self):
        input = "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_links(input), expected)

    def test_invalid_link_1(self):
        input = "This is [not]https://brokenlink.com/fake a link."
        self.assertEqual(extract_markdown_links(input), [])

    def test_invalid_link_2(self):
        input = "This is [not(https://brokenlink.com/fake) an image."
        self.assertEqual(extract_markdown_links(input), [])

    def test_invalid_link_3(self):
        input = "This is ![not](https://brokenlink.com/fake) a link."
        self.assertEqual(extract_markdown_links(input), [])

    def test_invalid_link_4(self):
        input = "This is ![not](https://brokenlink.com/fake) a link, but [this](https://image.com/image.png) is an image."
        expected = [("this", "https://image.com/image.png")]
        self.assertEqual(extract_markdown_links(input), expected)
