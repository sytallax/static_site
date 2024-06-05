from typing import Dict, List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: List["HTMLNode"] = [],
        props: Dict[str, str] = {},
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Converts the given HTMLNode into an HTML-friendly string"""
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Converts a dictionary of HTML properties into an
        HTML-friendly string"""

        result: str = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == self.props
        )
