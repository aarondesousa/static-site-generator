import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page


def main():
    static_dir = os.path.join(".", "static")
    public_dir = os.path.join(".", "public")
    content_md = os.path.join(".", "content", "index.md")
    template_path = os.path.join(".", "template.html")
    output_path = os.path.join(public_dir, "index.html")

    print(f'Deleting "{public_dir}"...')
    if os.path.exists(public_dir):
        if os.path.isdir(public_dir):
            shutil.rmtree(public_dir)
        elif os.path.isfile(public_dir):
            os.remove(public_dir)

    print(f'Copying files from "{static_dir}" to "{public_dir}"...')
    copy_files_recursive(static_dir, public_dir)

    print("Generating page...")
    generate_page(content_md, template_path, output_path)


if __name__ == "__main__":
    main()
