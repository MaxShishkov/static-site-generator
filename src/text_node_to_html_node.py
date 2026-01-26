from src.textnode import TextNode, TextType, TAGS
from src.htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    node = None
    match (text_node.text_type):
        case TextType.TEXT:
            node = LeafNode(None, text_node.text, None)
        case TextType.BOLD | TextType.ITALIC | TextType.CODE:
            node = LeafNode(TAGS[text_node.text_type], text_node.text, None)
        case TextType.LINK:
            node = LeafNode(TAGS[text_node.text_type], text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            node = LeafNode(TAGS[text_node.text_type], "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise AttributeError("Nodes text type is not one of the allowed types")
        
    return node