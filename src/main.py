import os
import shutil
import sys
from pathlib import Path

from copystatic import copy_static_to_public
from generate_page import generate_pages_recursive



dir_path_static = "./static"
dir_path_docs = "./docs"
content_src = "./content"
template_src = "./template.html"


def main():
    content_path = Path(content_src)
    dest_path = Path(dir_path_docs)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_static_to_public(dir_path_static, dir_path_docs)
    generate_pages_recursive(content_path, template_src, dest_path, basepath)

if __name__ == "__main__":
    main()