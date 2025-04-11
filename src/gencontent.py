import os
import re

from markdown_blocks import markdown_to_html_node


def generate_html_pages_recursive(source_dir_path, template_path, destination_dir_path):
    for entry in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, entry)
        destination_path = os.path.join(destination_dir_path, entry)

        if os.path.isfile(source_path):
            base, _ = os.path.splitext(destination_path)
            destination_path = base + ".html"
            generate_single_page(source_path, template_path, destination_path)

        elif os.path.isdir(source_path):
            generate_html_pages_recursive(source_path, template_path, destination_path)


def generate_single_page(source_markdown_path, template_path, destination_html_path):
    print(f" * {source_markdown_path} {template_path} -> {destination_html_path}")

    with open(source_markdown_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    destination_dir = os.path.dirname(destination_html_path)
    if destination_dir:
        os.makedirs(destination_dir, exist_ok=True)

    with open(destination_html_path, "w", encoding="utf-8") as f:
        f.write(output)


def extract_title(markdown):
    match = re.search(r"^#[ \t]+(.*)", markdown, re.MULTILINE)
    if not match:
        raise ValueError("no title found")
    return match.group(1)
