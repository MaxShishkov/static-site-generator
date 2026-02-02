import unittest

from src.markdown_to_html import *
from src.block_markdown import BlockType


class TestMakrdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_blockquote(self):
        md = """
> This is a quote
> with **bold** text
"""

        expected = "<div><blockquote><p>This is a quote with <b>bold</b> text</p></blockquote></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_ul(self):
        md = """
- first item
- second **bold** item
- third item with `code`
"""

        expected = "<div><ul><li>first item</li><li>second <b>bold</b> item</li><li>third item with <code>code</code></li></ul></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_ol(self):
        md = """
1. first item
2. second **bold** item
3. third item with `code`
"""

        expected = "<div><ol><li>first item</li><li>second <b>bold</b> item</li><li>third item with <code>code</code></li></ol></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_full_markdown_doc(self):
        md = """
# Title Heading

This is a **bold** and _italic_ paragraph
that spans multiple lines and has `code`.

> This is a quote
> with **bold** text

- first item
- second **bold** item
- third item with `code`

1. first ordered item
2. second _italic_ item
3. third item with [a link](https://example.com)

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        expected = "<div><h1>Title Heading</h1><p>This is a <b>bold</b> and <i>italic</i> paragraph that spans multiple lines and has <code>code</code>.</p><blockquote><p>This is a quote with <b>bold</b> text</p></blockquote><ul><li>first item</li><li>second <b>bold</b> item</li><li>third item with <code>code</code></li></ul><ol><li>first ordered item</li><li>second <i>italic</i> item</li><li>third item with <a href=\"https://example.com\">a link</a></li></ol><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )
        
    def test_normalize_text_p(self):
        text = "This is some text.\nThis is some more text.\nAnd more text"
        expected = "This is some text. This is some more text. And more text"
        result = normalize_text(BlockType.PARAGRAPH, text)
        self.assertEqual(result, expected)
        
    def test_normalize_text_h(self):
        text = "### This is some text."
        expected = "This is some text."
        result = normalize_text(BlockType.HEADING, text)
        self.assertEqual(result, expected)
    
    def test_normalize_text_bq(self):
        text = "> This is some text.\n> More text.\n> More text"
        expected = "This is some text. More text. More text"
        result = normalize_text(BlockType.QUOTE, text)
        self.assertEqual(result, expected)

    def test_normalize_text_ul(self):
        text = "- This is some text.\n- More text.\n- More text"
        expected = "This is some text.\nMore text.\nMore text"
        result = normalize_text(BlockType.UNORDERED_LIST, text)
        self.assertEqual(result, expected)
        
    def test_normalize_text_ol(self):
        text = "1. This is some text.\n2. More text.\n3. More text"
        expected = "This is some text.\nMore text.\nMore text"
        result = normalize_text(BlockType.ORDERED_LIST, text)
        self.assertEqual(result, expected)
        
    def test_get_tag_p(self):
        self.assertEqual("p", get_tag(BlockType.PARAGRAPH, "Hello"))
        
    def test_get_tag_h1(self):
        self.assertEqual("h1", get_tag(BlockType.HEADING, "# Hello"))
        
    def test_get_tag_h2(self):
        self.assertEqual("h2", get_tag(BlockType.HEADING, "## Hello"))
        
    def test_get_tag_h6(self):
        self.assertEqual("h6", get_tag(BlockType.HEADING, "###### Hello"))
