import os
import shutil

from copystatic import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print(f'Deleting "{dir_path_public}"...')
    if os.path.exists(dir_path_public):
        if os.path.isdir(dir_path_public):
            shutil.rmtree(dir_path_public)
        elif os.path.isfile(dir_path_public):
            os.remove(dir_path_public)

    print(f'Copying files from "{dir_path_static}" to "{dir_path_public}"...')
    copy_files_recursive(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
