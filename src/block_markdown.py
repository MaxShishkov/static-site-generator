from enum import Enum

class BlockType(Enum):
    PARAGRAPH           = "paragraph"
    HEADING             = "heading"
    CODE                = "code"
    QUOTE               = "quote"
    UNORDERED_LIST      = "unordered_list"
    ORDERED_LIST        = "ordered_list"

def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = []
    split_doc = markdown.split("\n\n")
    for line in split_doc:
        if line.strip():
            blocks.append(line.strip())
            
    return blocks
                     
def block_to_blocktype(text_block:str) -> BlockType:
    if text_block.startswith("#"):
        stripped = text_block.lstrip("#")
        count = len(text_block) - len(stripped)
        if 1 <= count <= 6 and stripped.startswith(" "):
            return BlockType.HEADING
    if text_block.startswith("```\n") and  text_block.endswith("\n```"):
        return BlockType.CODE
    
    split_text = text_block.split("\n")
    if text_block.startswith(">"):
        is_blockquote = True
        for text in split_text:
            if not text.startswith(">"):
                is_blockquote = False
                break
        if is_blockquote:
            return BlockType.QUOTE
    if text_block.startswith("- "):
        is_ul = True
        for text in split_text:
            if not text.startswith("- "):
                is_ul = False
                break
        if is_ul:
            return BlockType.UNORDERED_LIST
    if text_block.startswith("1. "):
        is_ol = True
        for index, text in enumerate(split_text):
            if not text.startswith(f"{index + 1}. "):
                is_ol = False
                break
        if is_ol:
            return BlockType.ORDERED_LIST
        
        
    for text in split_text:
        if not text.startswith(">"):
                is_blockquote = False
                break
        
        
    return BlockType.PARAGRAPH