import re
from typing import List, Tuple

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextNodeType


class MarkdownFormattingError(Exception):
    """A custom error representing incorrect Markdown formatting."""

    def __init__(self, markdown_text: str, message: str):
        self.markdown_text = markdown_text
        self.message = message
        super().__init__(message)


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """Extract Markdown image information from a string."""

    return re.findall(
        r"!\[(.*?)\]\((.*?)\)",  # Regex matches for Markdown images ( ![alt](link) )
        text,
    )


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """Extract Markdown link information from a string. Ignores images."""

    text_sanitized = text
    image = re.search(r"!\[(.*?)\]\((.*?)\)", text)
    if image:
        image_position_in_text = image.span()
        text_sanitized = (
            text[: image_position_in_text[0]] + text[image_position_in_text[1] :]
        )
    return re.findall(
        r"\[(.*?)\]\((.*?)\)",  # Regex matches for Markdown links ( [alt](link) )
        text_sanitized,
    )


def markdown_to_blocks(markdown: str) -> List[str]:
    """Separate a Markdown document into blocks.

    A Markdown block is separated by an empty line, which is represented
    as two newline (\\n) characters.
    """

    markdown_split_newline: List[str] = markdown.split("\n\n")
    markdown_split_newline_sanitized = [
        text.strip().lstrip("\n") for text in markdown_split_newline if text is not None
    ]
    return markdown_split_newline_sanitized


def block_to_block_type(markdown_block: str) -> str:
    """Calculate the type of Markdown block given."""

    if re.search(r"(?<!.)(#{1,6} )", markdown_block):
        return "heading"
    if re.search(r"^```", markdown_block) and re.search(r"```$", markdown_block):
        return "code"
    markdown_block_split = markdown_block.split("\n")
    if all(">" == x[0] for x in markdown_block_split):
        return "quote"
    if all("* " == x[:2] or "- " == x[:2] for x in markdown_block_split):
        return "unordered_list"
    is_block_ordered_list = True
    for i, block in enumerate(markdown_block_split):
        if f"{i+1}. " != block[:3]:
            is_block_ordered_list = False
    return "ordered_list" if is_block_ordered_list else "paragraph"


def markdown_to_html_node(markdown_document: str) -> HTMLNode:
    """Convert an entire Markdown file into a large div HTMLNode."""

    markdown_blocks = markdown_to_blocks(markdown_document)
    markdown_blocks_and_types = [
        (block, block_to_block_type(block)) for block in markdown_blocks
    ]
    block_type_conversion_map = {
        "heading": _heading_to_html_node,
        "code": _code_to_html_node,
        "quote": _quote_to_html_node,
        "unordered_list": _unordered_list_to_html_node,
        "ordered_list": _ordered_list_to_html_node,
        "paragraph": _paragraph_to_html_node,
    }
    blocks_to_html_nodes = [
        block_type_conversion_map[block_type](block)
        for block, block_type in markdown_blocks_and_types
    ]
    return ParentNode(blocks_to_html_nodes, "div")


def _heading_to_html_node(block: str) -> HTMLNode:
    """Convert a 'heading' Markdown block into an HTMLNode."""

    heading_text = block.lstrip("# ")
    heading_level = len(block) - len(heading_text) - 1
    textnodes = text_to_textnodes(heading_text)
    if len(textnodes) == 1:
        return LeafNode(heading_text, f"h{heading_level}")
    leaf_nodes = list(map(text_node_to_html_node, textnodes))
    return ParentNode(leaf_nodes, f"h{heading_level}")


def _code_to_html_node(block: str) -> HTMLNode:
    """Convert a 'code' Markdown block into an HTMLNode."""

    code_text = block.strip("`").strip()
    code_node = LeafNode(code_text, "code")
    return ParentNode([code_node], "pre")


def _quote_to_html_node(block: str) -> HTMLNode:
    """Convert a 'quote' Markdown block into an HTMLNode."""

    quote_text = block.replace(">", "").replace("\n ", " ").strip()
    return LeafNode(quote_text, "blockquote")


def _unordered_list_to_html_node(block: str) -> HTMLNode:
    """Convert an unordered list in Markdown into an HTMLNode."""

    ul_children = []
    list_text = block.split("\n")
    list_text = [x[2:] for x in list_text]
    textnodes = list(map(text_to_textnodes, list_text))
    for entry in textnodes:
        if len(entry) != 1:
            entry_as_html = list(map(text_node_to_html_node, entry))
            entry_as_li = ParentNode(entry_as_html, "li")
        else:
            entry_as_li = LeafNode(entry[0].text, "li")
        ul_children.append(entry_as_li)
    return ParentNode(ul_children, "ul")


def _ordered_list_to_html_node(block: str) -> HTMLNode:
    """Convert an ordered list in Markdown into an HTMLNode."""

    ol_children = []
    list_text = block.split("\n")
    list_text = [x[3:] for x in list_text]
    textnodes = list(map(text_to_textnodes, list_text))
    for entry in textnodes:
        if len(entry) != 1:
            entry_as_html = list(map(text_node_to_html_node, entry))
            entry_as_li = ParentNode(entry_as_html, "li")
        else:
            entry_as_li = LeafNode(entry[0].text, "li")
        ol_children.append(entry_as_li)
    return ParentNode(ol_children, "ol")


def _paragraph_to_html_node(block: str) -> HTMLNode:
    """Convert a paragraph in Markdown into an HTMLNode."""

    block_sanitized = block.strip("\n").strip().replace("\n", " ")
    block_textnode = text_to_textnodes(block_sanitized)
    if len(block_textnode) == 1:
        if block_textnode[0].text_type == TextNodeType.LINK and block_textnode[0].url:
            return LeafNode(
                block_textnode[0].text, "a", {"href": block_textnode[0].url}
            )
        if block_textnode[0].text_type == TextNodeType.IMAGE and block_textnode[0].url:
            return LeafNode(
                "", "img", {"src": block_textnode[0].url, "alt": block_textnode[0].text}
            )
        return LeafNode(block_sanitized, "p")
    block_as_html = list(map(text_node_to_html_node, block_textnode))
    return ParentNode(block_as_html, "p")


def extract_title(markdown_document: str) -> str:
    """Return the title text of a Markdown file."""

    mardown_in_blocks = markdown_to_blocks(markdown_document)
    for block in mardown_in_blocks:
        if re.search(r"(?<!.)(# )", block):
            return block[2:]
    raise MarkdownFormattingError(
        markdown_text=markdown_document, message="Markdown document has no title"
    )


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextNodeType
) -> List[TextNode]:
    """Separate Markdown syntax operations from a TextNode of type
    'text' into its applicable type."""

    output: List[TextNode] = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            output.append(node)
            continue
        node_split_by_delimiter = node.text.split(delimiter)
        if len(node_split_by_delimiter) == 1:
            output.append(node)
            continue
        if len(node_split_by_delimiter) == 2:
            raise MarkdownFormattingError(
                markdown_text=node.text,
                message="Invalid Markdown syntax. No closing delimiter.",
            )
        new_textnodes = [
            TextNode(node_text, TextNodeType.TEXT)
            if node_split_by_delimiter.index(node_text) % 2
            == 0  # Regular TextNodes will be index 0 and 2
            else TextNode(
                node_text, TextNodeType(text_type)
            )  # New type node will be index 1
            for node_text in node_split_by_delimiter
        ]
        output.extend([x for x in new_textnodes if x.text])

    return output


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """Split TextNodes which contain Markdown images into separate
    TextNodes."""

    output: List[TextNode] = []
    for node in old_nodes:
        node_split: List[TextNode] = []
        if not isinstance(node, TextNode):
            output.append(node)
            continue
        images_in_node = extract_markdown_images(node.text)
        if not images_in_node:
            output.append(node)
            continue
        for i, image in enumerate(images_in_node):
            alt = image[0]
            link = image[1]
            node_with_image_removed: List[str] = node.text.split(f"![{alt}]({link})", 1)
            node_split.append(TextNode(node_with_image_removed[0], TextNodeType.TEXT))
            node_split.append(TextNode(alt, TextNodeType.IMAGE, link))
            if i == len(images_in_node) - 1:
                node_split.append(
                    TextNode(node_with_image_removed[1], TextNodeType.TEXT)
                )
            else:
                node = TextNode(node_with_image_removed[1], TextNodeType.TEXT)
        output.extend(node_split)

    return [x for x in output if x.text]


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """Split TextNodes which contain Markdown links into separate
    TextNodes."""

    output: List[TextNode] = []
    for node in old_nodes:
        node_split: List[TextNode] = []
        if not isinstance(node, TextNode):
            output.append(node)
            continue
        links_in_node = extract_markdown_links(node.text)
        if not links_in_node:
            output.append(node)
            continue
        for i, link_data in enumerate(links_in_node):
            alt = link_data[0]
            link = link_data[1]
            node_text_split: List[str] = node.text.split(f"[{alt}]({link})", 1)
            node_split.append(TextNode(node_text_split[0], TextNodeType.TEXT))
            node_split.append(TextNode(alt, TextNodeType.LINK, link))
            if i == len(links_in_node) - 1:
                node_split.append(TextNode(node_text_split[1], TextNodeType.TEXT))
            else:
                node = TextNode(node_text_split[1], TextNodeType.TEXT)
        output.extend(node_split)

    return [x for x in output if x.text]


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """Converts given TextNode to its corresponding HTMLNode according
    to its text_type."""

    conversion_map = {
        TextNodeType.TEXT: LeafNode(value=text_node.text),
        TextNodeType.BOLD: LeafNode(tag="b", value=text_node.text),
        TextNodeType.ITALIC: LeafNode(tag="i", value=text_node.text),
        TextNodeType.CODE: LeafNode(tag="code", value=text_node.text),
        TextNodeType.LINK: LeafNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url} if text_node.url else {},
        ),
        TextNodeType.IMAGE: LeafNode(
            tag="img",
            value="",
            props={
                "src": text_node.url if text_node.url else "",
                "alt": text_node.text,
            },
        ),
    }

    return conversion_map[text_node.text_type]


def text_to_textnodes(text: str) -> List[TextNode]:
    """Convert a string of text into TextNodes"""

    nodes: List[TextNode] = [TextNode(text, TextNodeType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
