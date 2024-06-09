import os
from markdown_operations import extract_title, markdown_to_html_node


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


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
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
