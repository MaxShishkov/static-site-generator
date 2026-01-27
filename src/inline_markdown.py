from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0: #no closing delimiter
            raise Exception("Invalide Markdown syntax")
        
        if split_text == [""]:
            new_nodes.append(TextNode("", TextType.TEXT))
            continue
        
        for i in range(len(split_text)):
            if i % 2 == 0: #text
                if split_text[i] != "":
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else: #inside delimiter
                new_nodes.append(TextNode(split_text[i], text_type))
                
    return new_nodes