import os
import shutil
import sys

from copystatic import copy_static_files_recursive
from gencontent import generate_html_pages_recursive


def main():
    args = sys.argv
    basepath = args[1] if len(args) >= 2 else "/"

    source_static_dir = os.path.join(".", "static")
    source_content_dir = os.path.join(".", "content")
    destination_public_dir = os.path.join(".", "docs")
    template_file_path = os.path.join(".", "template.html")

    print(f'Deleting "{destination_public_dir}"...')
    if os.path.exists(destination_public_dir):
        if os.path.isdir(destination_public_dir):
            shutil.rmtree(destination_public_dir)
        elif os.path.isfile(destination_public_dir):
            os.remove(destination_public_dir)

    print(
        f'Copying static files from "{source_static_dir}" to "{destination_public_dir}"...'
    )
    copy_static_files_recursive(source_static_dir, destination_public_dir)

    print("Generating HTML pages...")
    generate_html_pages_recursive(
        source_content_dir, template_file_path, destination_public_dir, basepath
    )


if __name__ == "__main__":
    main()
