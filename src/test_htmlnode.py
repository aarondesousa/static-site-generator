import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


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
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty_or_none(self):
        node = HTMLNode("p", "this is a paragraph", None, None)
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode("p", "this is a paragraph", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_node_initialization(self):
        node = HTMLNode("span", "Some span text")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Some span text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("a", "this is a link", None, {"href": "https://www.google.com"})
        self.assertEqual(
            repr(node),
            "HTMLNode(a, this is a link, children: None, {'href': 'https://www.google.com'})",
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
            repr(node),
            "HTMLNode(div, this is a div, children: [HTMLNode(a, this is a link, children: None, {'href': 'https://www.google.com'}), HTMLNode(h1, this is a heading, children: None, None)], None)",
        )

    # test leaf nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode(
            "div",
            "This is a div",
            {"class": "something", "href": "https://www.google.com"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="something" href="https://www.google.com">This is a div</div>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), "Some text")

    # test parent nodes
    def test_parent_to_html_with_child(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Child 1"),
                LeafNode(
                    "span",
                    "Child 2",
                    {"class": "something 1", "href": "https://www.google.com"},
                ),
                LeafNode(None, "Child 3"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><b>Child 1</b><span class="something 1" href="https://www.google.com">Child 2</span>Child 3</div>',
        )

    def test_parent_to_html_with_nested_child(self):
        node = ParentNode(
            "section",
            [ParentNode("div", [LeafNode("span", "span text")], {"id": "parent"})],
            {"class": "wrapper"},
        )
        self.assertEqual(
            node.to_html(),
            '<section class="wrapper"><div id="parent"><span>span text</span></div></section>',
        )

    def test_parent_to_html_with_nested_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode("span", [LeafNode(None, "grandchild")]),
                ParentNode("span", [LeafNode("i", "grandchild 2")]),
            ],
            {"class": "the div"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="the div"><span>grandchild</span><span><i>grandchild 2</i></span></div>',
        )


if __name__ == "__main__":
    unittest.main()
