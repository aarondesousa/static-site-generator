import os
import shutil


def copy_files_recursive(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for filename in os.listdir(source):
        source_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        print(f" * {source_path} -> {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            copy_files_recursive(source_path, dest_path)
