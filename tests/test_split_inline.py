import unittest

from src.split_inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimeter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType


class TestSplitInline(unittest.TestCase):
    # Tests for the text to textnodes function
    def test_text_to_textnodes_plain(self):
        text = "Just plain text"
        self.assertListEqual(
            text_to_textnodes(text), [TextNode("Just plain text", TextType.TEXT)]
        )

    def test_text_to_textnode_all_types(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Q4.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Q4.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def unclosed_delimeter_raises_on_text_to_textnode(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This has an **unclosed bold")

    def test_text_to_textnode_only_bold(self):
        text = "**just bold**"
        self.assertListEqual(
            text_to_textnodes(text), [TextNode("just bold", TextType.BOLD)]
        )

    def test_text_to_textnode_with_multiple_same_types(self):
        text = "**bold1** and **bold2**"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
        )

    # Tests for the splits noted delimeter function
    def test_bold(self):
        node = TextNode("This is a **bold** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is an _italic_ text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "_", TextType.ITALIC),
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code(self):
        node = TextNode("This is a `code` text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "`", TextType.CODE),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_no_delimeter(self):
        node = TextNode("Yep nothing to see here", TextType.TEXT)
        self.assertEqual(split_nodes_delimeter([node], "**", TextType.BOLD), [node])

    def test_multiple(self):
        node = TextNode("**a** and **b**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node], "**", TextType.BOLD),
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_unclosed_delimeter_raises(self):
        node = TextNode("I am an unclosed **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimeter([node], "**", TextType.BOLD)

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(split_nodes_delimeter([node], "**", TextType.BOLD), [node])

    def test_mixed_node_list(self):
        nodes = [
            TextNode(
                'Look at this python code `print("Hello, world!")`', TextType.TEXT
            ),
            TextNode("It should print: ", TextType.TEXT),
            TextNode("Hello, world!", TextType.BOLD),
        ]
        self.assertEqual(
            split_nodes_delimeter(nodes, "`", TextType.CODE),
            [
                TextNode("Look at this python code ", TextType.TEXT),
                TextNode('print("Hello, world!")', TextType.CODE),
                TextNode("It should print: ", TextType.TEXT),
                TextNode("Hello, world!", TextType.BOLD),
            ],
        )

    # Tests for the extract markdown images function
    def test_extract_single_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_miltiple_markdown_images(self):
        matches = extract_markdown_images("![alt1](url1.png) and ![alt2](url2.png)")
        self.assertListEqual(matches, [("alt1", "url1.png"), ("alt2", "url2.png")])

    def test_textract_no_images(self):
        matches = extract_markdown_images("This is just some regular text")
        self.assertListEqual(matches, [])

    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](/images/hello.png)")
        self.assertListEqual(matches, [("", "/images/hello.png")])

    def test_ignores_links(self):
        matches = extract_markdown_images("This is a [link](google.com) not an image")
        self.assertListEqual(matches, [])

    # Tests for the extract markdown links function
    def test_extract_single_markdown_link(self):
        matches = extract_markdown_links("Click [here](google.com) to search it")
        self.assertListEqual(matches, [("here", "google.com")])

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "I have [to google](google.com) and [to youtube](youtube.com)"
        )
        self.assertListEqual(
            matches, [("to google", "google.com"), ("to youtube", "youtube.com")]
        )

    def test_no_links(self):
        matches = extract_markdown_links("Some old regular text")
        self.assertListEqual(matches, [])

    def test_ignore_images(self):
        matches = extract_markdown_links("![Awesome](awesome.png)")
        self.assertListEqual(matches, [])

    def test_mixed_images_and_links(self):
        matches = extract_markdown_links(
            "![image](img.png) and [link](https://boot.dev)"
        )
        self.assertListEqual(matches, [("link", "https://boot.dev")])

    # Tests for the split nodes image function
    def test_split_nodes_img_no_input(self):
        self.assertListEqual(split_nodes_image([]), [])

    def test_split_nodes_single_img(self):
        node = TextNode(
            "Check out this cool image ![Awesome pic](images/cool.png)", TextType.TEXT
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("Check out this cool image ", TextType.TEXT),
                TextNode("Awesome pic", TextType.IMAGE, "images/cool.png"),
            ],
        )

    def test_split_nodes_multiple_img(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_image_at_start(self):
        node = TextNode("![image](url.png) is at the start", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("image", TextType.IMAGE, "url.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode("text ends with an image ![image](url.png)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("text ends with an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
            ],
        )

    def test_only_images_no_surrounding_text(self):
        node = TextNode("![image](url.png)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("image", TextType.IMAGE, "url.png")],
        )

    def test_no_images_pass_through(self):
        node = TextNode("Just plain text, nothing to split.", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_text_with_link_but_no_image_passthrough(self):
        node = TextNode(
            "This has a [link](https://boot.dev) but no image.", TextType.TEXT
        )
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_non_text_node_passthrough_for_img_split(self):
        node = TextNode("bold text", TextType.BOLD)
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("Text with ![img](url.png)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("More plain text", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
                TextNode("already bold", TextType.BOLD),
                TextNode("More plain text", TextType.TEXT),
            ],
        )

    def test_empty_alt_text_img_split(self):
        node = TextNode("![](url.png)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("", TextType.IMAGE, "url.png")],
        )

    # Tests for the split nodes link function
    def test_split_nodes_link_no_input(self):
        self.assertListEqual(split_nodes_link([]), [])

    def test_split_nodes_single_link(self):
        node = TextNode("This is text with a [link](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_nodes_multiple_links(self):
        node = TextNode(
            "[to boot dev](https://boot.dev) and [to youtube](https://youtube.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("to boot dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://youtube.com"),
            ],
        )

    def test_link_at_start(self):
        node = TextNode("[link](url.com) is at the start", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" is at the start", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode("text ends with a [link](url.com)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("text ends with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
        )

    def test_only_link_no_surrounding_text(self):
        node = TextNode("[link](url.com)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("link", TextType.LINK, "url.com")],
        )

    def test_no_links_passthrough_links(self):
        node = TextNode("Just plain text, nothing to split.", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [node])

    def test_with_image_but_no_link_passthrough(self):
        node = TextNode("This has an ![image](url.png) but no link.", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [node])

    def test_non_text_node_passthrough_for_link_split(self):
        node = TextNode("italic text", TextType.ITALIC)
        self.assertListEqual(split_nodes_link([node]), [node])

    # Test chaining both functions
    def test_link_and_image_mixed_in_same_sentence(self):
        node = TextNode(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        node_after_img_split = split_nodes_image([node])
        expected = split_nodes_link(node_after_img_split)
        self.assertListEqual(
            expected,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
