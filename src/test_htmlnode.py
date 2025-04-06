import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "this is a link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "this is a paragraph")
        self.assertEqual("", node.props_to_html())

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "this is a paragraph", None, {})
        self.assertEqual("", node.props_to_html())

    def test_node_initialization(self):
        node = HTMLNode("span", "Some span text")
        self.assertEqual("span", node.tag)
        self.assertEqual("Some span text", node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)

    def test_repr(self):
        node = HTMLNode("a", "this is a link", None, {"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(a, this is a link, children: None, {'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_repr_nested_children(self):
        node = HTMLNode(
            "div",
            "this is a div",
            [
                HTMLNode(
                    "a", "this is a link", None, {"href": "https://www.google.com"}
                ),
                HTMLNode("h1", "this is a heading"),
            ],
        )
        self.assertEqual(
            "HTMLNode(div, this is a div, children: [HTMLNode(a, this is a link, children: None, {'href': 'https://www.google.com'}), HTMLNode(h1, this is a heading, children: None, None)], None)",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()
