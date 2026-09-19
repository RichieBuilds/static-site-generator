from src.blocktype import BlockType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.split_block import block_to_block_type, markdown_to_blocks
from src.split_inline import text_to_textnodes
from src.textnode import TextNode, TextType


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html_node(block))
    return ParentNode("div", nodes)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children


def heading_to_html_node(block: str) -> HTMLNode:
    hashes, text = block.split(" ", 1)
    level = len(hashes)
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)


def paragraph_to_html_node(block: str) -> HTMLNode:
    text = block.replace("\n", " ")
    children = text_to_children(text)

    return ParentNode("p", children)


def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    text = block[3:-3]
    text = text.split("\n", 1)[1]

    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])

    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    html_items = []

    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    html_items = []

    for line in lines:
        text = line.split(" ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(text_node.text, tag="code")
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Link TextNode must have a url")
            return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Image TextNode must have a url")
            return LeafNode(
                "", tag="img", props={"src": text_node.url, "alt": text_node.text}
            )
