from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    node = TextNode("This is some alt text", TextType.IMAGE, "https://www.google.com")
    print(node)
    node = HTMLNode(
        "a",
        "this is a link",
        None,
        {
            "href": "https://www.google.com",
            "target": "_blank",
        },
    )
    print(node)
    print(node.props_to_html())


main()
