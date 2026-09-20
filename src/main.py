import logging
import sys

from src.copy_static import copy_static_to_public
from src.generate_pages import generate_pages_recursive, normalize_basepath

CONTENT_DIR = "content"
STATIC_DIR = "static"
PUBLIC_DIR = "docs"
TEMPLATE_PATH = "template.html"

logger = logging.getLogger(__name__)

# TODO: Add exceptions.py
def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )

    logger.info("Site Generation Started!")

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    basepath = normalize_basepath(basepath)
    
    copy_static_to_public(STATIC_DIR, PUBLIC_DIR)

    logger.info("Beginning recursive page generation")
    
    generate_pages_recursive(CONTENT_DIR, PUBLIC_DIR, TEMPLATE_PATH, basepath)
    
    logger.info("Concluding recursive page generation")
    logger.info("Site Generation Finished!")

if __name__ == "__main__":
    main()
