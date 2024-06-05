import re
import os
from typing import List, Tuple
from textnode import TextNode

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """Extract Markdown image information from a string."""
    return re.findall(
        # Regex matches for Markdown images ( ![alt](link) )
        r"!\[(.*?)\]\((.*?)\)",
        text,
    )


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """Extract Markdown link information from a string. Ignores images."""
    image = re.search(r"!\[(.*?)\]\((.*?)\)", text)
    if image:
        image_position = image.span()
        text = text[: image_position[0]] + text[image_position[1] :]
    return re.findall(
        # Regex matches for Markdown links ( [alt](link) )
        r"\[(.*?)\]\((.*?)\)",
        text,
    )


def markdown_to_blocks(markdown: str) -> List[str]:
    """Separate a Markdown document into blocks. A Markdown block is
    separated by an empty line, which is two newline characters."""
    markdown_split_newline: List[str] = markdown.split("\n\n")
    markdown_split_newline_sanitized = [
        x.strip().lstrip("\n") for x in markdown_split_newline if x
    ]
    return markdown_split_newline_sanitized


def block_to_block_type(markdown_block: str):
    """Calculate the type of block given"""
    if re.search(r"(?<!.)(#{1,6} )", markdown_block):
        return "heading"
    if re.search(r"^```", markdown_block) and re.search(r"```$", markdown_block):
        return "code"
    markdown_block_split = markdown_block.split("\n")
    if all([">" == x[0] for x in markdown_block_split]):
        return "quote"
    if all(["* " == x[:2] or "- " == x[:2] for x in markdown_block_split]):
        return "unordered_list"
    is_block_ordered_list = True
    for i in range(len(markdown_block_split)):
        if f"{i+1}. " != markdown_block_split[i][:3]:
            is_block_ordered_list = False
    return "ordered_list" if is_block_ordered_list else "paragraph"


def markdown_to_html_node(markdown_document: str) -> HTMLNode:
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
        block_type_conversion_map[block[1]](block[0])
        for block in markdown_blocks_and_types
    ]
    return ParentNode(blocks_to_html_nodes, "div")


def _heading_to_html_node(block: str) -> HTMLNode:
    heading_text = block.lstrip("# ")
    heading_level = len(block) - len(heading_text) - 1
    textnodes = text_to_textnodes(heading_text)
    if len(textnodes) == 1:
        return LeafNode(heading_text, f"h{heading_level}")
    leaf_nodes = list(map(text_node_to_html_node, textnodes))
    return ParentNode(leaf_nodes, f"h{heading_level}")


def _code_to_html_node(block: str) -> HTMLNode:
    code_text = block.strip("`").strip()
    code_node = LeafNode(code_text, "code")
    return ParentNode([code_node], "pre")


def _quote_to_html_node(block: str) -> HTMLNode:
    quote_text = block.replace(">", "").replace("\n ", " ").strip()
    return LeafNode(quote_text, "blockquote")


def _unordered_list_to_html_node(block: str) -> HTMLNode:
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
    block_sanitized = block.strip("\n").strip().replace("\n", " ")
    block_textnode = text_to_textnodes(block_sanitized)
    if len(block_textnode) == 1:
        if block_textnode[0].text_type == "link" and block_textnode[0].url:
            return LeafNode(
                block_textnode[0].text, "a", {"href": block_textnode[0].url}
            )
        if block_textnode[0].text_type == "image" and block_textnode[0].url:
            return LeafNode(
                "", "img", {"src": block_textnode[0].url, "alt": block_textnode[0].text}
            )
        return LeafNode(block_sanitized, "p")
    block_as_html = list(map(text_node_to_html_node, block_textnode))
    return ParentNode(block_as_html, "p")


def extract_title(markdown_document: str):
    mardown_in_blocks = markdown_to_blocks(markdown_document)
    for block in mardown_in_blocks:
        if re.search(r"(?<!.)(# )", block):
            return block[2:]
    raise Exception("Markdown document has no title")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_file = f.read()
    with open(template_path) as f:
        template_file = f.read()
    generated_page = markdown_to_html_node(markdown_file).to_html()
    page_title = extract_title(markdown_file)
    generated_file_with_title = template_file.replace("{{ Title }}", page_title)
    generated_file_with_body = generated_file_with_title.replace(
        "{{ Content }}", generated_page
    )
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "x") as f:
        f.write(generated_file_with_body)


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    """Separate Markdown syntax operations from a TextNode of type
    'text' into its applicable type."""

    output: List[TextNode] = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            output.append(node)
            continue
        node_split = node.text.split(delimiter)
        if len(node_split) == 1:
            output.append(node)
            continue
        if len(node_split) == 2:
            raise Exception("Invalid Markdown syntax. No closing delimiter.")
        new_textnodes = [
            TextNode(x, "text")
            if node_split.index(x) % 2 == 0  # Regular TextNodes will be index 0 and 2
            else TextNode(x, text_type)  # New type node will be index 1
            for x in node_split
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
        for index in range(0, len(images_in_node)):
            alt = images_in_node[index][0]
            link = images_in_node[index][1]
            node_text_split: List[str] = node.text.split(f"![{alt}]({link})", 1)
            node_split.append(TextNode(node_text_split[0], "text"))
            node_split.append(TextNode(alt, "image", link))
            if index == len(images_in_node) - 1:
                node_split.append(TextNode(node_text_split[1], "text"))
            else:
                node = TextNode(node_text_split[1], "text")
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
        for index in range(0, len(links_in_node)):
            alt = links_in_node[index][0]
            link = links_in_node[index][1]
            node_text_split: List[str] = node.text.split(f"[{alt}]({link})", 1)
            node_split.append(TextNode(node_text_split[0], "text"))
            node_split.append(TextNode(alt, "link", link))
            if index == len(links_in_node) - 1:
                node_split.append(TextNode(node_text_split[1], "text"))
            else:
                node = TextNode(node_text_split[1], "text")
        output.extend(node_split)

    return [x for x in output if x.text]


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """Converts given TextNode to its corresponding HTMLNode according
    to its text_type."""

    conversion_map = {
        "text": LeafNode(value=text_node.text),
        "bold": LeafNode(tag="b", value=text_node.text),
        "italic": LeafNode(tag="i", value=text_node.text),
        "code": LeafNode(tag="code", value=text_node.text),
        "link": LeafNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url} if text_node.url else {},
        ),
        "image": LeafNode(
            tag="img",
            value="",
            props={
                "src": text_node.url if text_node.url else "",
                "alt": text_node.text,
            },
        ),
    }

    if text_node.text_type not in conversion_map:
        raise Exception("TextNode type unknown")

    return conversion_map[text_node.text_type]


def text_to_textnodes(text: str) -> List[TextNode]:
    """Convert a string of text into TextNodes"""

    nodes: List[TextNode] = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    if not all(map(os.path.exists, (dir_path_content, template_path, dest_dir_path))):
        raise Exception("Attemped to search directory that doesn't exist")
    directory_contents = os.listdir(dir_path_content)
    for item in directory_contents:
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            dest_path = os.path.join(dest_dir_path, item.split(".")[0] + ".html")
            generate_page(item_path, template_path, dest_path)
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path)

