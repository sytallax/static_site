from typing import Dict, List, Optional
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """An HTML node that has children, needed for recursion"""

    def __init__(
        self,
        children: List["HTMLNode"],
        tag: Optional[str] = None,
        props: Dict[str, str] = {},
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode has no children")
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output
