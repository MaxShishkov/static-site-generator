from src.block_markdown import *
from src.htmlnode import HTMLNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.text_node_to_html_node import text_node_to_html_node
from src.textnode import TextNode, TextType

    
BLOCK_TAGS = {
    BlockType.PARAGRAPH: "p",
    BlockType.HEADING: "h",
    BlockType.CODE: "code",
    BlockType.QUOTE: "blockquote",
    BlockType.UNORDERED_LIST: "ul",
    BlockType.ORDERED_LIST: "ol",
}

def normalize_text(block_type:BlockType, text:str) -> str:
    if block_type == BlockType.PARAGRAPH:
        text = text.replace("\n", " ")
        
    if block_type == BlockType.HEADING:
        text = text.lstrip("#")
        text = text.lstrip()
        
    if block_type == BlockType.CODE:
        lines = text.splitlines()
        text = "\n".join(lines[1:-1])
        text += "\n"
        
    if block_type == BlockType.QUOTE:
        clean_lines = []
        lines = text.splitlines()
        for line in lines:
            line = line.lstrip()
            if line.startswith(">"):
                line = line[1:]
            line = line.lstrip()
            clean_lines.append(line)   
        text = " ".join(clean_lines).strip()
        
    if block_type == BlockType.UNORDERED_LIST:
        clean_lines = []
        lines = text.splitlines()
        for line in lines:
            line = line.lstrip()
            if line.startswith("- "):
                line = line[2:]
            line = line.lstrip()
            if line != "":
                clean_lines.append(line)
        text = "\n".join(clean_lines)
        
    if block_type == BlockType.ORDERED_LIST:
        clean_lines = []
        lines = text.splitlines()
        for line in lines:
            line = line.lstrip()
            line = line[2:]
            line = line.lstrip()
            if line != "":
                clean_lines.append(line)
        text = "\n".join(clean_lines)
        
    return text

def text_to_children(text:str):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        html_nodes.append(node)
    return html_nodes
    
def get_tag(block_type:BlockType, text:str) -> str:
    if block_type == BlockType.HEADING:
        count = len(text) - len(text.lstrip("#"))
        tag = BLOCK_TAGS[block_type] + str(count)
        return tag
    else:
        return BLOCK_TAGS[block_type]

def textblock_to_htmlnode(block_type: BlockType, text:str) -> HTMLNode:
    props = None
    
    tag = get_tag(block_type, text)
    text = normalize_text(block_type, text)
    if block_type == BlockType.CODE:
        code_text_node = TextNode(text, TextType.CODE, None)
        code_node = text_node_to_html_node(code_text_node)
        parent_node = ParentNode("pre",[code_node], None)   
    else:
        if block_type == BlockType.QUOTE:
            children = text_to_children(text)
            p_node = ParentNode("p", children, None)
            children = [p_node]
        elif block_type == BlockType.UNORDERED_LIST:
            children = []
            lines = text.splitlines()
            for line in lines:
                nodes = text_to_children(line)
                children.append(ParentNode("li", nodes, None))
        elif block_type == BlockType.ORDERED_LIST:
            children = []
            lines = text.splitlines()
            for line in lines:
                nodes = text_to_children(line)
                children.append(ParentNode("li", nodes, None))
        else:
            children = text_to_children(text)
                
            
        
        parent_node = ParentNode(tag, children, props)
    
    
    return parent_node
    
    

def markdown_to_html_node(markdown:str) -> HTMLNode:
    text_blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in text_blocks:
        block_type = block_to_blocktype(block)
        html_node = textblock_to_htmlnode(block_type, block)
        children.append(html_node)
    
    parent_Node = ParentNode("div", children, None)
    return parent_Node
            