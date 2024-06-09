from copy_directory_contents import copy_directory_contents
from page_generator import generate_pages_recursive


def main():
    copy_directory_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
