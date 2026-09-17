import re

from src.textnode import TextNode, TextType


def split_nodes_delimeter(old_nodes: list[TextNode], delimeter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split = node.text.split(delimeter)
        # Even elements mean no closing delimeter
        if len(split) % 2 == 0:
            raise ValueError(f"Unclosed delimeter in {node!r}")
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    if not old_nodes:
        return new_nodes
        
    for current_node in old_nodes:
        if current_node.text_type != TextType.TEXT:
            new_nodes.append(current_node)
            continue
            
        current_text = current_node.text
        matches = extract_markdown_images(current_text)

        if not matches:
            new_nodes.append(current_node)
            continue
            
        for match in matches:
            img_alt, img_url = match
            delimeter = f"![{img_alt}]({img_url})"
            segments = current_text.split(delimeter, maxsplit=1)

            if len(segments) != 2:
                raise ValueError("invalid markdown, image setion not closed")
                
            text_node = TextNode(segments[0], TextType.TEXT)
            img_node = TextNode(img_alt, TextType.IMAGE, img_url)

            if text_node.text:
                new_nodes.append(text_node)
            new_nodes.append(img_node)
            current_text = segments[1]

        lastly = TextNode(current_text, TextType.TEXT)
        if lastly.text:
            new_nodes.append(lastly)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    if not old_nodes:
        return new_nodes

    for current_node in old_nodes:
        if current_node.text_type != TextType.TEXT:
            new_nodes.append(current_node)
            continue

        current_text = current_node.text
        matches = extract_markdown_links(current_text)

        if not matches:
            new_nodes.append(current_node)
            continue

        for match in matches:
            link_text, link_url = match
            delimeter = f"[{link_text}]({link_url})"
            segments = current_text.split(delimeter, maxsplit=1)

            if len(segments) != 2:
                raise ValueError("invalid markdown, link section not closed")

            text_node = TextNode(segments[0], TextType.TEXT)
            link_node = TextNode(link_text, TextType.LINK, link_url)

            if text_node.text:
                new_nodes.append(text_node)
            new_nodes.append(link_node)
            current_text = segments[1]

        lastly = TextNode(current_text, TextType.TEXT)
        if lastly.text:
            new_nodes.append(lastly)

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)