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

    def test_text_node_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_bold(self):
        node = TextNode("Hello", TextType.BOLD)
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")


    def test_text_node_itallic(self):
        node = TextNode("Hello", TextType.ITALIC)
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_code(self):
        node = TextNode("Hello", TextType.CODE)
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_link(self):
        node = TextNode("Hello", TextType.LINK, "boot.dev")
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "boot.dev"})
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_image(self):
        node = TextNode("Hello", TextType.IMAGE, "/images/boot.png")
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "/images/boot.png", "alt": "Hello"})


if __name__ == "__main__":
    unittest.main()
