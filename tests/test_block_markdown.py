import unittest

from src.block_markdown import BlockType
from src.block_markdown import markdown_to_blocks, block_to_blocktype


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_heading(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
    
    def test_markdown_to_blocks_link_image(self):
        md = """
# This is a heading

## Another heading

This is a paragraph with a [link](https://www.google.com)

This is a paraagraph with an image ![Description of image](url/of/image.jpg)
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "## Another heading",
                "This is a paragraph with a [link](https://www.google.com)",
                "This is a paraagraph with an image ![Description of image](url/of/image.jpg)",
            ],
        )
        
        
    def test_markdown_to_blocks_code(self):
        md = """
# This is a heading

```
def func():
    print("hello")
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "```\ndef func():\n    print(\"hello\")\n```",
            ],
        )
        
    def test_markdown_to_blocks_whitespace(self):
        md = """                        
                            
                                
                                           
"""
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(blocks,[])
        
    def test_markdown_to_blocks_empty_str(self):
        md = ""
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(blocks,[])
        
        
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_blocktype_heading(self):
        block = "# Heading"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.HEADING)
        
    def test_block_to_blocktype_heading2(self):
        block = "## Heading"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.HEADING)
        
    def test_block_to_blocktype_heading6(self):
        block = "###### Heading"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.HEADING)
        
    def test_block_to_blocktype_heading7(self):
        block = "####### Heading"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_blocktype_code(self):
        block = "```\npring(\"hello\")\n```"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.CODE)
        
    def test_block_to_blocktype_quote(self):
        block = "> some quoute here"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.QUOTE)
        
    def test_block_to_blocktype_quote_multy(self):
        block = "> some quoute here\n> quote continues\n> more quote"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.QUOTE)
        
    def test_block_to_blocktype_ul(self):
        block = "- item1"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_blocktype_ul_mult(self):
        block = "- item1\n- item2\n- item3"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_blocktype_ol(self):
        block = "1. item1"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.ORDERED_LIST)
        
    def test_block_to_blocktype_ol_mult(self):
        block = "1. item1\n2. item2\n3. item3"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.ORDERED_LIST)
        
    def test_block_to_blocktype_ol_bad_format(self):
        block = "1. item1\n2. item2\n4. item3"
        block_type = block_to_blocktype(block)
        
        self.assertIs(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_blocktype_quote_bad_format(self):
        block = "> some quoute here\n quote continues\n more quote"
        block_type = block_to_blocktype(block)

        self.assertIs(block_type, BlockType.PARAGRAPH)
    
if __name__ == "__main__":
    unittest.main()