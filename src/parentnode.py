from typing import override

from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, 
        tag: str,  
        children: list[HTMLNode], 
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    @override
    def to_html(self)-> str:
        if self.tag is None:
            raise ValueError("Parent node tag attribute is None. Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node children attribute is None. Parent node must have children")

        html_string = "".join(child.to_html() for child in self.children)
        attributes = self.props_to_html()
        return f"<{self.tag}{attributes}>{html_string}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"ParentNode(tag: {self.tag}, children: {self.children}, props: {self.props})"
