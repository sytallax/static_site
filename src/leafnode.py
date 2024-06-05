from typing import Dict, Optional
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: Optional[str] = None,
        props: Dict[str, str] = {},
    ) -> None:
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self) -> str:
        if not self.value:
            if self.tag != "img":
                raise ValueError("Leaf node has no value")
        if not self.tag and self.value:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
