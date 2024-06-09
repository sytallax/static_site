from typing import Dict, List, Optional


class HTMLNode:
    """A generic representation of a block of HTML code."""

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

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
        return f"HTMLNode(tag={self.tag}, " \
               f"value={self.value}, " \
               f"children={self.children}, " \
               f"props={self.props})" \

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == self.props
        )
