import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_text_not_eq(self):
        node1 = TextNode("My name is node1", TextType.TEXT)
        node2 = TextNode("My name is node2", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_test_type_not_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("THis is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_url_not_eq(self):
        node1 = TextNode("This ia a link node", TextType.LINK)
        node2 = TextNode("This is a link node", TextType.LINK, url="boot.dev")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()