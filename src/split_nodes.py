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