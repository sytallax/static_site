import unittest

from markdown_operations import extract_markdown_images


class TestExtractMarkdownFromImages(unittest.TestCase):
    def test_one_image(self):
        input = "This is text with ![an](https://image.com/image.png) image."
        expected = [("an", "https://image.com/image.png")]
        self.assertEqual(extract_markdown_images(input), expected)

    def test_two_images(self):
        input = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_images(input), expected)

    def test_invalid_image_1(self):
        input = "This is [not](https://brokenlink.com/fake) an image."
        self.assertEqual(extract_markdown_images(input), [])

    def test_invalid_image_2(self):
        input = "This is ![not](https://brokenlink.com/fake an image."
        self.assertEqual(extract_markdown_images(input), [])

    def test_invalid_image_3(self):
        input = "This is ![not(https://brokenlink.com/fake) an image."
        self.assertEqual(extract_markdown_images(input), [])
