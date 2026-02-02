import unittest

from src.generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")
        
    def test_extract_title_mdfile(self):
        md = """
# Title

Some text here

This is a paraagraph with an image ![Description of image](url/of/image.jpg)
"""
        title = extract_title(md)
        self.assertEqual(title, "Title")
        
    def test_extract_title_no_title(self):
        md = "Hello"
        with self.assertRaises(Exception):
            title = extract_title(md)
        
if __name__ == "__main__":
    unittest.main()
