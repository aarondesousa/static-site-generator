import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with **two** bolded **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bolded ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
        )

    def test_delim_bold_double_consecutive(self):
        node = TextNode(
            "**This** **is** text with consecutive **bolded** **words**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" text with consecutive ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text **with two** bolded **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text ", TextType.TEXT),
                TextNode("with two", TextType.BOLD),
                TextNode(" bolded ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_bold_and_code(self):
        node = TextNode(
            "This is text with some **bold text** and a `code block` with some more **bold text here**",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with some ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" with some more ", TextType.TEXT),
                TextNode("bold text here", TextType.BOLD),
            ],
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italicized_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italicized", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    # tests for images and links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and [another link](https://www.example.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("link", "https://www.google.com"),
                ("another link", "https://www.example.com"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
