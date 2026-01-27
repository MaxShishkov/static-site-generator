import unittest

from src.textnode import TextNode, TextType
from src.inline_markdown import split_nodes_delimiter
from src.inline_markdown import extract_markdown_images, extract_markdown_links



class TestSplitNodeDelim(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, result_list)
        
        
    def test_split_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, result_list)
        
    def test_split_italic_block(self):
        node = TextNode("This is text with a _bold block_ word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, result_list)
        
    def test_split_exception(self):
        node = TextNode("This is text with a _bold block word", TextType.TEXT)
        
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
    def test_split_just_text(self):
        node = TextNode("This is text with with no delimiters", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result_list = [
            TextNode("This is text with with no delimiters", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, result_list)
        
        
    def test_split_multiple_blocks(self):
        node = TextNode("This is text with a **bold block** word **bold block**", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
        ]
        
        self.assertEqual(new_nodes, result_list)
        
    def test_split_delimiter_at_start(self):
        node = TextNode("**bold block** This is text with a word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("bold block", TextType.BOLD),
            TextNode(" This is text with a word", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, result_list)
        
    def test_split_delimiter_at_end(self):
        node = TextNode("This is text with a word **bold block**", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("This is text with a word ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
        ]
        
        self.assertEqual(new_nodes, result_list)
        
    def test_split_not_text_type(self):
        node = TextNode("`code block`", TextType.CODE)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(new_nodes, [TextNode("`code block`", TextType.CODE)])
        
    def test_split_empty_string_text_node(self):
        node = TextNode("", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, result_list)
        
    def test_split_empty_string_in_delimiter(self):
        node = TextNode("This is text with a **** word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, result_list)
        
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        
        self.assertEqual(result, expected)
        
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, matches)
        
    def test_extract_markdown_images_no_match(self):
        text = "This is text with a  and "
        result = extract_markdown_images(text)
        
        self.assertEqual(result, [])
        
    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        
        self.assertEqual(result, expected)
        
    def test_extract_markdown_links(self):
        text = "This is text with a link [to example dev](https://www.example.dev)"
        result = extract_markdown_links(text)
        expected = [
            ("to example dev", "https://www.example.dev"),
        ]
        
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()