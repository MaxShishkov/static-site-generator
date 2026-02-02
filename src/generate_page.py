import os
from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            line = line.lstrip("#")
            line = line.lstrip()
            line = line.rstrip()
            return line
    
    raise Exception("Markdown has no h1 header")
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    print(f"* Reading markdown file {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
        
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    html_node = markdown_to_html_node(markdown)
    html_str = html_node.to_html()
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    
    dirname = os.path.dirname(dest_path)
    os.makedirs(dirname, exist_ok=True)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)