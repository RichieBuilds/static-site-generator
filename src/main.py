import logging

from src.copy_static import copy_static_to_public
from src.generate_page import generate_page

CONTENT_DIR = "content"
STATIC_DIR = "static"
PUBLIC_DIR = "public"
TEMPLATE_PATH = "template.html"

# TODO: Add exceptions.py


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )
    copy_static_to_public(STATIC_DIR, PUBLIC_DIR)

    generate_page(f"{CONTENT_DIR}/index.md", f"{PUBLIC_DIR}/index.html", TEMPLATE_PATH)


if __name__ == "__main__":
    main()
