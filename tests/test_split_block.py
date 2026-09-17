import unittest

from src.split_block import markdown_to_blocks


class TestSplitBlock(unittest.TestCase):
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
        self.assertListEqual(
            markdown_to_blocks("        \n\n       \n\n       "),
            []
        )

    def test_windows_new_line(self):
        markdown = "First block\r\n\r\nSecond block"
        self.assertListEqual(
            markdown_to_blocks(markdown),
            ["First block", "Second block"]
        )

    def test_whitespace_only_black_line(self):
        markdown = "First block\n    \nSecond block"
        self.assertListEqual(
            markdown_to_blocks(markdown),
            ["First block", "Second block"]
        )