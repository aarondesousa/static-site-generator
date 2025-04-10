import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def split_nodes_image_and_link(old_nodes, text_type, extract_markdown_elements):
    new_nodes = []
    image_prefix = "!" if text_type == TextType.IMAGE else ""
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        items = extract_markdown_elements(text)
        if len(items) == 0:
            new_nodes.append(old_node)
            continue
        for item in items:
            item_text, item_url = item
            sections = text.split(f"{image_prefix}[{item_text}]({item_url})", 1)
            if len(sections) != 2:
                raise ValueError(
                    f"invalid markdown, {text_type.value} section not closed"
                )
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(item_text, text_type, item_url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_image_and_link(
        old_nodes, TextType.IMAGE, extract_markdown_images
    )


def split_nodes_link(old_nodes):
    return split_nodes_image_and_link(old_nodes, TextType.LINK, extract_markdown_links)


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
