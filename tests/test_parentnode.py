import unittest

from src.htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        html_str = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), html_str)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        html_str = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(
            parent_node.to_html(),
            html_str,
        )
        
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode("", [child_node]).to_html()
            
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node]).to_html()
            
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", []).to_html()
            
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()
            
    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        html_str = "<p><b>Bold text</b>Normal text<i>italic text</i></p>"
        self.assertEqual(node.to_html(), html_str)
        
    def test_to_html_with_grandgrandchildren(self):
        grandgrand_node = LeafNode("b", "grandgrandchild")
        grandchild_node = ParentNode("p", [grandgrand_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        html_str = "<div><span><p><b>grandgrandchild</b></p></span></div>"
        self.assertEqual(parent_node.to_html(),html_str)
        
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        html_str = "<div class=\"container\"><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), html_str)
        
    def test_to_html_mixed_nesting(self):
        node = ParentNode(
            "p",
            [
                ParentNode("p", [LeafNode(None, "Normal text")]),
                LeafNode("b", "Bold text"),
                ParentNode("p", [LeafNode("i", "italic text")]),
                LeafNode(None, "Normal text"),
            ],
        )
        
        html_str = "<p><p>Normal text</p><b>Bold text</b><p><i>italic text</i></p>Normal text</p>"
        self.assertEqual(node.to_html(), html_str)
        
    def test_to_html_lists(self):
        node = ParentNode(
            "ul",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode("b", "item1"),
                        LeafNode(None, " - description")
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("b", "item2"),
                        LeafNode(None, " - description")
                    ]
                )
            ]
        )
        
        html_str = "<ul><li><b>item1</b> - description</li><li><b>item2</b> - description</li></ul>"
        self.assertEqual(node.to_html(), html_str)
        
    def test_assign_value(self):
        node = ParentNode("", "Hello, world!")
        with self.assertRaises(AttributeError):
            node.value = "test"
        
    def test_ParentNode_repr(self):
        tag = "a"
        prop = {"href": "https://www.example.com"}
        children = [LeafNode(None, "text")]
        node = ParentNode(tag, children, prop)
        
        repr_str = f"ParentNode({tag}, {children}, {prop})"
        self.assertEqual(repr(node), repr_str)

if __name__ == "__main__":
    unittest.main()