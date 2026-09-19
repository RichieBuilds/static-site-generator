import logging
import os

from src.markdown_to_html import extract_title, markdown_to_html_node

logger = logging.getLogger(__name__)


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