from typing import override


class HTMLNode:
    tag: str | None
    value: str | None
    children: list["HTMLNode"] | None
    props: dict[str, str] | None

    def __init__(self, 
        tag: str | None = None, 
        value: str | None = None,
        children: list["HTMLNode"] | None = None, 
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    @override
    def __repr__(self) -> str:
        return f'HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})'

    def to_html(self):
        raise NotImplementedError("Not Implemented yet")

    def props_to_html(self) -> str:
        attributes = []
        if not self.props:
            return ""

        for key in self.props:
            attributes.append(f'{key}="{self.props[key]}"')
            
        return f' {" ".join(attributes)}'