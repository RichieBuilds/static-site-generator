import re

from src.blocktype import BlockType


def markdown_to_blocks(markdown: str) -> list[str]:
    markdown = markdown.replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n", markdown)
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        final_blocks.append(block)
    return final_blocks

def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    elif re.match(r"^```.*\n[\s\S]*```$", markdown):
        return BlockType.CODE
    elif all(re.match(r"^>", line) for line in markdown.split("\n")):
        return BlockType.QUOTE
    elif all(re.match(r"^-", line) for line in markdown.split("\n")):
       return BlockType.UNORDERED_LIST
    elif all(
        re.match(rf"^{i + 1}\. ", line)
        for i, line in enumerate(markdown.split("\n"))
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH