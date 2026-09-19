import unittest

from src.markdown_to_html import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_headings(self):
        md = """
# This is an h1

## This is an h2 with **bold** text

###### This is an h6
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><h2>This is an h2 with <b>bold</b> text</h2><h6>This is an h6</h6></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> spanning multiple lines
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
- and _italic_ text
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>italic</i> text</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. with items
3. and **bold** text
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with items</li><li>and <b>bold</b> text</li></ol></div>",
        )

    def test_links_and_images(self):
        md = """
This paragraph has a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This paragraph has a <a href="https://boot.dev">link</a> and an <img src="https://i.imgur.com/zjjcJKZ.png" alt="image"></img></p></div>',
        )

    def test_mixed_document(self):
        md = """
# Heading one

This is a paragraph with `code` in it.

> A quote here

- Item one
- Item two

1. First
2. Second

```
raw code
stays raw
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading one</h1>"
            "<p>This is a paragraph with <code>code</code> in it.</p>"
            "<blockquote>A quote here</blockquote>"
            "<ul><li>Item one</li><li>Item two</li></ul>"
            "<ol><li>First</li><li>Second</li></ol>"
            "<pre><code>raw code\nstays raw\n</code></pre>"
            "</div>",
        )
