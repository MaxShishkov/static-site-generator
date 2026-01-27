import unittest

from src.textnode import TextNode, TextType
from src.inline_markdown import split_nodes_delimiter
from src.inline_markdown import extract_markdown_images, extract_markdown_links
from src.inline_markdown import split_nodes_image, split_nodes_link



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
        
        self.assertEqual(new_nodes, [])
        
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
        text = "This is text with a link [to boot dev](https://www.example.dev) and [to youtube](https://www.youtube.com)"
        result = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.example.dev"),
            ("to youtube", "https://www.youtube.com"),
        ]
        
        self.assertEqual(result, expected)
        
    def test_extract_markdown_links(self):
        text = "This is text with a link [to example dev](https://www.example.dev)"
        result = extract_markdown_links(text)
        expected = [
            ("to example dev", "https://www.example.dev"),
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_node_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" link.", TextType.TEXT),
                
            ],
            new_nodes,
        )
        
    def test_split_node_image_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an image.", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_node_image_end(self):
        node = TextNode(
            "This is text with an image. ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an image. ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
        
    def test_split_node_image_end_space(self):
        node = TextNode(
            "This is text with an image. ![image](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an image. ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_node_image_multiple_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_node_image_no_link(self):
        node = TextNode(
            "This is text with no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with no image.", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_node_image_not_text_node(self):
        node = TextNode(
            "`code`",
            TextType.CODE,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("`code`", TextType.CODE),

            ],
            new_nodes,
        )
        
    def test_split_node_image_no_alt(self):
        node = TextNode(
            "This is text with an image. ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an image. ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
        
    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link. [link text](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link. ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
        
    def test_split_node_link_multiple(self):
        node = TextNode(
            "This is text with a link. [link text](https://example.com) and another [another link text](https://link.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link. ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("another link text", TextType.LINK, "https://link.dev"),
            ],
            new_nodes,
        )
        
    def test_split_node_link_start(self):
        node = TextNode(
            "[link text](https://example.com) This is text with a link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" This is text with a link.", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_node_link_middle(self):
        node = TextNode(
            "This is text with a [link text](https://example.com) link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" link.", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_node_link_no_link(self):
        node = TextNode(
            "This is text with a link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link.", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_node_link_not_text_node(self):
        node = TextNode(
            "`code`",
            TextType.CODE,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("`code`", TextType.CODE),

            ],
            new_nodes,
        )
        
        
if __name__ == "__main__":
    unittest.main()