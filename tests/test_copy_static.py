import os
import tempfile
import unittest

from src.copy_static import copy_static_to_public, rdel


class TestCopyStatic(unittest.TestCase):
    def test_copies_single_file(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            with open(os.path.join(src_dir, "style.css"), "w+") as f:
                f.write("body {color: red; }")

            copy_static_to_public(src_dir, dst_dir)

            copied_path = os.path.join(dst_dir, "style.css")
            self.assertTrue(os.path.exists(copied_path))

            with open(copied_path) as f:
                self.assertEqual(f.read(), "body {color: red; }")

    def test_wipes_stale_content_in_dst(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            with open(os.path.join(src_dir, "new.css"), "w") as f:
                f.write("body {color: red; }")

            # Simulate leftover content from a previous copy
            with open(os.path.join(dst_dir, "old.css"), "w") as f:
                f.write("body {color: blue; }")

            copy_static_to_public(src_dir, dst_dir)

            self.assertFalse(os.path.exists(os.path.join(dst_dir, "old.css")))
            self.assertTrue(os.path.exists(os.path.join(dst_dir, "new.css")))

    def test_empty_src_produces_empty_dst(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            copy_static_to_public(src_dir, dst_dir)
            
            self.assertEqual(os.listdir(dst_dir), [])

    def test_rdel_removes_existing_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = os.path.join(temp_dir, "to_del")
            os.mkdir(target)

            with open(os.path.join(target, "file.txt"), "w") as f:
                f.write("foo")

            rdel(target)
            
            self.assertFalse(os.path.exists(target))
    
if __name__ == "__main__":
    unittest.main()
