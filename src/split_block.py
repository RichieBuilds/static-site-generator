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
    match markdown:
        case re.findall(r"^#{1, 6} "):
            return BlockType.HEADING
        