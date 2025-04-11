from enum import Enum
import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case _:
            raise ValueError(f"invalid markdown block: {block}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    match = re.match(r"^(#{1,6})[ \t]+(.*)", block)
    if not match:
        raise ValueError(f"invalid heading block: {block}")
    hashes, content = match.groups()
    tag = f"h{len(hashes)}"
    return ParentNode(tag, text_to_children(content))


def code_to_html_node(block):
    text_node = TextNode(block[4:-3], TextType.TEXT)
    return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(text_node)])])


def quote_to_html_node(block):
    matches = re.findall(r"^>[ \t]*(.*)", block, re.MULTILINE)
    text = " ".join(matches)
    return ParentNode("blockquote", text_to_children(text))


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    child_nodes = []
    for line in lines:
        child_nodes.append(ParentNode("li", text_to_children(line[3:])))
    return ParentNode("ol", child_nodes)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    child_nodes = []
    for line in lines:
        child_nodes.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", child_nodes)
