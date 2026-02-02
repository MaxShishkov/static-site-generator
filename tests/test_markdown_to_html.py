import unittest

from src.markdown_to_html import markdown_to_html_node


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
