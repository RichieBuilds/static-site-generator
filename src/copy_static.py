import logging
import os
import shutil

logger = logging.getLogger(__name__)

# Main function to copy from static dir to public dir
def copy_static_to_public(src: str, dst: str) -> None:
    logger.info("Starting static copy: '%s' -> '%s'", src, dst)
    logger.info("Starting delete of old directory: '%s'", dst)
    
    rdel(dst)
    os.mkdir(dst)
    rcopy(src, dst)
    
    logger.info("Finished static copy")


# Helper Function to Recursively copy
def rcopy(src: str, dst: str) -> None:
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        item_dst_path = os.path.join(dst, item)

        if os.path.isfile(item_path):
            shutil.copy(item_path, item_dst_path)
            logger.info("Copied %s from: %s to: %s", item, item_path, item_dst_path)
        else:
            if not os.path.exists(item_dst_path):
                os.mkdir(item_dst_path)
                logger.info("Created directory '%s'", item_dst_path)
            rcopy(item_path, item_dst_path)


# Helper function to recursively delete
def rdel(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
        logger.info("Deleted old directory '%s'", path)
    else:
        logger.info("'%s' does not exist, deletion skipped", path)
