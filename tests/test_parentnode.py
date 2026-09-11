import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_no_children(self):
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ]
        )
        
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_no_tag(self):
        child = LeafNode(tag="p", value="Hello")
        parent = ParentNode(tag=None, children=[child]) 
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_repr(self):
        child = LeafNode(tag="p", value="Hello")
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(
            repr(parent),
            "ParentNode(tag: div, children: [LeafNode(tag: p, value: Hello, props: None)], props: None)"
        )

if __name__ == "__main__":
    unittest.main()