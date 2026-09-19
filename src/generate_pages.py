import logging
import os

from src.markdown_to_html import extract_title, markdown_to_html_node

logger = logging.getLogger(__name__)


def generate_pages_recursive(src: str, dest: str, template_path: str) -> None:
    logger.info("Scanning '%s' dir", src)
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            item = os.path.splitext(item)[0]
            if item == "index":
                page_dest = os.path.join(dest, "index.html")
            else:
                page_dest = os.path.join(dest, item, "index.html")

            generate_page(item_path, page_dest, template_path)
        else:
            new_dest = os.path.join(dest, item)
            generate_pages_recursive(item_path, new_dest, template_path)
    logger.info("Finished '%s' dir", src)

def generate_page(src: str, dest: str, template_path: str) -> None:
    logger.info(
        "Generating page from '%s' to '%s' using '%s'", src, dest, template_path
    )

    with (
        open(src, "r") as f,
        open(template_path, "r") as t,
    ):
        markdown = f.read()
        template = t.read()

    page_title = extract_title(markdown)
    html_string = markdown_to_html_node(markdown).to_html()

    html_doc = template.replace("{{ Title }}", page_title)
    html_doc = html_doc.replace("{{ Content }}", html_string)

    logger.info("Page generation done")

    dest_dir = os.path.dirname(dest)

    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        logger.info("Created directory '%s'", dest_dir)

    with open(dest, "w") as f:
        logger.info("Writing page to '%s'", dest)

        f.write(html_doc)

    logger.info("DONE! Page generated and written at '%s'", dest)