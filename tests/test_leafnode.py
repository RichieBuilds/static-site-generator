import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_tag(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("Hello")
        self.assertEqual(node.to_html(), "Hello")

    def teast_leaf_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click me", props={"href": "https://google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com">Click me</a>'
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode(value=None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("Hello", "p")
        self.assertEqual(
            repr(node),
            "LeafNode(tag: p, value: Hello, props: None)"
        )

if __name__ == "__main__":
    unittest.main()