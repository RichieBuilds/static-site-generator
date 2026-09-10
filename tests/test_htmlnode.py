import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", props={"src": "img.png"})
        self.assertEqual(node.props_to_html(), ' src="img.png"')
    
    def test_props_to_html_multiple_props(self):
        node = HTMLNode("a", "google", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: p, value: hello, children: None, props: None)"
        )

    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

if __name__ == "__main__":
    unittest.main()
