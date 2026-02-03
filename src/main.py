import os
import shutil
from copystatic import copy_static_to_public
from generate_page import generate_pages_recursive
from pathlib import Path

dir_path_static = "./static"
dir_path_public = "./public"
content_src = "./content"
template_src = "./template.html"
html_dest = "./public"


def main():
    copy_static_to_public(dir_path_static, dir_path_public)
    
    content_path = Path(content_src)
    dest_path = Path(html_dest)
    generate_pages_recursive(content_path, template_src, dest_path)

if __name__ == "__main__":
    main()