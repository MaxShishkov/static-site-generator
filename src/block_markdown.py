def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = []
    split_doc = markdown.split("\n\n")
    for line in split_doc:
        if line.strip():
            blocks.append(line.strip())
            
    return blocks
            