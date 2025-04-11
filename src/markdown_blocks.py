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
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_nodes.append(ParentNode("p", text_to_children(block)))
                # print(f"block nodes: {block_nodes}")
            case BlockType.HEADING:
                match = re.match(r"^(#{1,6})[ \t]+(.*)", block)
                if match:
                    hashes, content = match.groups()
                    tag = f"h{len(hashes)}"
                    block_nodes.append(ParentNode(tag, text_to_children(content)))
            case BlockType.CODE:
                text_node = TextNode(block[4:-3], TextType.TEXT)
                # print(f"text node: {repr(text_node)}")
                block_nodes.append(
                    ParentNode(
                        "pre", [ParentNode("code", [text_node_to_html_node(text_node)])]
                    )
                )
            case BlockType.QUOTE:
                lines = block.split("\n")
                child_nodes = []
                first = True
                for line in lines:
                    if first:
                        child_nodes.extend(text_to_children(line[2:]))
                        first = False
                    else:
                        child_nodes.extend(text_to_children(line[1:]))
                block_nodes.append(ParentNode("blockquote", child_nodes))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                child_nodes = []
                for line in lines:
                    child_nodes.append(ParentNode("li", text_to_children(line[3:])))
                block_nodes.append(ParentNode("ol", child_nodes))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                child_nodes = []
                for line in lines:
                    child_nodes.append(ParentNode("li", text_to_children(line[2:])))
                block_nodes.append(ParentNode("ul", child_nodes))
            case _:
                raise ValueError(f"invalid markdown block: {block}")

    # parent_node = ParentNode("div", block_nodes)
    # print(f"parent node: {parent_node}")
    # print(f"html: {repr(parent_node.to_html())}")
    return ParentNode("div", block_nodes)


def text_to_children(text):
    # print(f"text: {text}")
    new_text = text.replace("\n", " ")
    # print(f"text-after: {new_text}")
    text_nodes = text_to_textnodes(new_text)
    # print(f"text_nodes: {text_nodes}")
    html_nodes = []
    for text_node in text_nodes:
        # html_node = text_node_to_html_node(text_node)
        # print(f"html node: {html_node}")
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
