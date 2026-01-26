import unittest

from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        html_str = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), html_str)
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "test", {"href": "https://www.example.com"})
        html_str = "<a href=\"https://www.example.com\">test</a>"
        self.assertEqual(node.to_html(), html_str)
        
    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
           LeafNode("a", "", {"href": "https://www.example.com"}).to_html()

            
        with self.assertRaises(ValueError):
            LeafNode("a", None, {"href": "https://www.example.com"}).to_html()


    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "Hello, world!")
        html_str = "Hello, world!"
        self.assertEqual(node.to_html(), html_str)
        
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), html_str)
        
    def test_assign_children(self):
        node = LeafNode("", "Hello, world!")
        with self.assertRaises(AttributeError):
            node.children = ["test"]
            
    def test_LeafNode_repr(self):
        tag = "a"
        value = "test"
        prop = {"href": "https://www.example.com"}
        node = LeafNode(tag, value, prop)
        
        repr_str = f"LeafNode({tag}, {value}, {prop})"
        self.assertEqual(repr(node), repr_str)
        
    def test_leaf_to_html_img(self):
        tag = "img"
        value = ""
        property = {"src": "address.com", "alt": "alt text"}
        node = LeafNode(tag, value, property)
        html_str = node.to_html()
        
        self.assertTrue(html_str.startswith("<img"))
        self.assertTrue(html_str.endswith("/>"))

        self.assertIn('src="address.com"', html_str)
        self.assertIn('alt="alt text"', html_str)