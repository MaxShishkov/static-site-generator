import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_None(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.tag, None)
        
    def test_init(self):
        tag = "p"
        value = "test"
        child = HTMLNode("a", "test2", None, {"href": "html://example.com"})
        children = [child]
        prop = None
        node = HTMLNode(tag, value, children, prop)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, prop)
        
        
    def test_HTMLNode_repr(self):
        tag = "p"
        value = "test"
        child = HTMLNode("a", "test2", None, {"href": "html://example.com"})
        children = [child]
        prop = None
        node = HTMLNode(tag, value, children, prop)
        
        repr_str = f"HTMLNode({tag}, {value}, {children}, {prop})"
        self.assertEqual(repr(node), repr_str)
        
    def test_prop_to_html_None(self):
        tag = "p"
        value = "test"
        children = None
        prop = None
        node = HTMLNode(tag, value, children, prop)
        
        self.assertEqual(node.props_to_html(), "")
        
    def test_prop_to_html(self):
        tag = "a"
        value = "test"
        children = None
        prop = {"href": "https://www.example.com", "target": "_blank",}
        node = HTMLNode(tag, value, children, prop)
        html_str = " href=\"https://www.example.com\" target=\"_blank\""
        
        self.assertEqual(node.props_to_html(), html_str)
