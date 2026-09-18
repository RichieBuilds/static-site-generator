import unittest

from src.blocktype import BlockType
from src.split_block import block_to_block_type, markdown_to_blocks


class TestSplitBlock(unittest.TestCase):
    # Tests for markdown to block function
    def test_single_block(self):
        markdown = "Just a single paragraph with no breaks."
        self.assertListEqual(
            markdown_to_blocks(markdown),
            ["Just a single paragraph with no breaks."],
        )

    def test_multiple_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_leading_and_white_space_stripped(self):
        markdown = """
            First block

Second block

Last block
            """
        self.assertListEqual(
            markdown_to_blocks(markdown),
            ["First block", "Second block", "Last block"],
        )

    def test_multiple_cosecutive_blank_lines(self):
        markdown = """
Hello





there
        """
        self.assertListEqual(
            markdown_to_blocks(markdown),
            ["Hello", "there"],
        )

    def test_empty_string(self):
        self.assertListEqual(markdown_to_blocks(""), [])

    def test_only_white_space(self):
        self.assertListEqual(markdown_to_blocks("        \n\n       \n\n       "), [])

    def test_windows_new_line(self):
        markdown = "First block\r\n\r\nSecond block"
        self.assertListEqual(
            markdown_to_blocks(markdown), ["First block", "Second block"]
        )

    def test_whitespace_only_black_line(self):
        markdown = "First block\n    \nSecond block"
        self.assertListEqual(
            markdown_to_blocks(markdown), ["First block", "Second block"]
        )

    # Tests for block to block type function
    def test_block_to_heading(self):
        block = "# I am a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_code(self):
        block = """```py
print("Hello")
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_quote(self):
        block = ">First quote\n>Second quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_unordered_list(self):
        block = "- This\n- is an\n- unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. item one"), BlockType.ORDERED_LIST)

    def test_block_to_ordered_list_multiple_items(self):
        block = "1. Item one\n2. Item two\n3. Item three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_ordered_list_wrong_start_is_paragraph(self):
        block = "2. Item one\n3. Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_ordered_list_skipped_number_is_paragraph(self):
        block = "1. Item one\n3. Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_ordered_list_out_of_order_is_paragraph(self):
        block = "1. item one\n2. item two\n2. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_paragraph(self):
        block = "This is just a regular paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_paragraph_multiline(self):
        block = "This is line one\nand this continues on line two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
