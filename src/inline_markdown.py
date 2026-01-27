from src.textnode import TextNode, TextType
import re

DELIMS = {
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`",
}

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0: #no closing delimiter
            raise Exception("Invalide Markdown syntax")
        
        for i in range(len(split_text)):
            if i % 2 == 0: #text
                if split_text[i] != "":
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else: #inside delimiter
                new_nodes.append(TextNode(split_text[i], text_type))
                
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        markdown_list = extract_markdown_images(node.text)
        
        if not markdown_list:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        split_nodes = []
        
        for item in markdown_list:
            image_alt, image_link = item
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]
            
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
            
        if split_nodes:
            new_nodes.extend(split_nodes)
            
    return  new_nodes
            

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        markdown_list = extract_markdown_links(node.text)
        
        if not markdown_list:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        split_nodes = []
        
        for item in markdown_list:
            link_text, link_src = item
            sections = original_text.split(f"[{link_text}]({link_src})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            split_nodes.append(TextNode(link_text, TextType.LINK, link_src))
            original_text = sections[1]
            
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
            
        if split_nodes:
            new_nodes.extend(split_nodes)
            
    return  new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type in TextType:
        if text_type == TextType.TEXT:
            continue
        if text_type == TextType.IMAGE:
            nodes = split_nodes_image(nodes)
        elif text_type == TextType.LINK:
            nodes = split_nodes_link(nodes)
        else:
            nodes = split_nodes_delimiter(nodes, DELIMS[text_type], text_type)
            
    return nodes