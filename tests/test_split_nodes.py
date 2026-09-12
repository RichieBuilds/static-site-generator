from platform import node
import unittest

from src.split_nodes import split_nodes_delimeter
from src.textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a **bold** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_italic(self):
        node = TextNode("This is an _italic_ text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "_", TextType.ITALIC),
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_code(self):
        node = TextNode("This is a `code` text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], '`', TextType.CODE),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_no_delimeter(self):
        node = TextNode("Yep nothing to see here", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [node]
        )

    def test_multiple(self):
        node = TextNode("**a** and **b**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD)
            ]
        )

    def test_unclosed_delimeter_raises(self):
        node = TextNode("I am an unclosed **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimeter([node], "**", TextType.BOLD)

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [node]
        )

    def test_mixed_node_list(self):
        nodes = [
            TextNode('Look at this python code `print("Hello, world!")`', TextType.TEXT),
            TextNode("It should print: ", TextType.TEXT),
            TextNode("Hello, world!", TextType.BOLD)
        ]
        self.assertEqual(
            split_nodes_delimeter(nodes, "`", TextType.CODE),
            [
                TextNode("Look at this python code ", TextType.TEXT),
                TextNode('print("Hello, world!")', TextType.CODE),
                TextNode("It should print: ", TextType.TEXT),
                TextNode("Hello, world!", TextType.BOLD)
            ]
        )

if __name__ == "__main__":
    unittest.main()