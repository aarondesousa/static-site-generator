import os
import shutil


def copy_static_files_recursive(source_dir_path, destination_dir_path):
    if not os.path.exists(destination_dir_path):
        os.makedirs(destination_dir_path, exist_ok=True)

    for entry in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, entry)
        destination_path = os.path.join(destination_dir_path, entry)
        print(f" * {source_path} -> {destination_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy_static_files_recursive(source_path, destination_path)
