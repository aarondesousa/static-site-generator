from textnode import TextNode, TextType


def main():
    node = TextNode("This is some alt text", TextType.IMAGE, "https://www.google.com")
    print(node)


main()
