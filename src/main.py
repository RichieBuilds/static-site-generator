import logging

from src.copy_static import copy_static_to_public

STATIC_DIR = "static"
PUBLIC_DIR = "public"

# TODO: Add exceptions.py


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )
    copy_static_to_public(STATIC_DIR, PUBLIC_DIR)

if __name__ == "__main__":
    main()
