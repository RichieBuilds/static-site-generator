from typing import override

from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    
    def __init__(
        self, 
        value: str, 
        tag: str | None = None, 
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node value attribute is None. Leaf node must have a value")
        if self.tag is None:
            return self.value
        attributes = self.props_to_html()
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"