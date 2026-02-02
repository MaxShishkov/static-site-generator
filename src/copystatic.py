import os
import shutil


def clean_dir(path):
    if os.path.exists(path):
        print("Deleting public directory...")
        shutil.rmtree(path)
    print("Creating public directory...")
    os.mkdir(path)
    
def copy_dir_tree(src, dest):
    file_list = os.listdir(src)
    for file in file_list:
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)
        print(f" * {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_dir_tree(src_path, dest_path)

def copy_static_to_public(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    
    clean_dir(dest)
    print("Copying static files to public directory...")
    copy_dir_tree(src, dest)

