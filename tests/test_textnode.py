import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        text = "This is a text node"
        url = "http://example.com"
        node = TextNode(text, TextType.BOLD, url)
        
        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, url)
    
    def test_eq(self):
        text = "This is a text node"
        node = TextNode(text, TextType.BOLD)
        node2 = TextNode(text, TextType.BOLD)
        self.assertEqual(node, node2)


    def test_eq_url_none(self):
        text = "This is a text node"
        node = TextNode(text, TextType.BOLD)
        node2 = TextNode(text, TextType.BOLD)
        self.assertEqual(node.url, node2.url)
        self.assertEqual(node.url, None)
        self.assertEqual(node2.url, None)
        
    def test_eq_with_url(self):
        text = "This is a text node"
        url = "http://example.com"
        node = TextNode(text, TextType.BOLD, url)
        node2 = TextNode(text, TextType.BOLD, url)
        self.assertEqual(node, node2)
        self.assertEqual(node.url, url)
        self.assertEqual(node2.url, url)
        
    def test_not_eq(self):
        node = TextNode("text1", TextType.BOLD, "http://url1")
        node2 = TextNode("text2", TextType.BOLD, "http://url2")
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        result = "TextNode(text1, bold, http://url1)"
        node = TextNode("text1", TextType.BOLD, "http://url1")
        self.assertEqual(repr(node), result)
        
if __name__ == "__main__":
    unittest.main()