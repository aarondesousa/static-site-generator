import unittest

from htmlnode import HTMLNode, LeafNode


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

    def test_props_to_html_empty_or_none(self):
        node = HTMLNode("p", "this is a paragraph", None, None)
        self.assertEqual("", node.props_to_html())
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

    # test leaf nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual("<p>Hello, world!</p>", node.to_html())

    def test_leaf_to_html_div(self):
        node = LeafNode(
            "div",
            "This is a div",
            {"class": "something", "href": "https://www.google.com"},
        )
        self.assertEqual(
            '<div class="something" href="https://www.google.com">This is a div</div>',
            node.to_html(),
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual("Some text", node.to_html())


if __name__ == "__main__":
    unittest.main()
