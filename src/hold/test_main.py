import unittest
import filecmp

from main import copy_static, generate_page

class TestMain(unittest.TestCase):
    def test_copy_static(self):
        copy_static("/home/lazlo/StaticSite/static", "/home/lazlo/StaticSite/public/")
        self.assertTrue(filecmp.cmp("/home/lazlo/StaticSite/static/index.css", "/home/lazlo/StaticSite/public/index.css", shallow=False))
        self.assertTrue(filecmp.cmp("/home/lazlo/StaticSite/static/images/tolkien.png", "/home/lazlo/StaticSite/public/images/tolkien.png", shallow=False))
    
    def test_generate_page(self):
        generate_page("/home/lazlo/StaticSite/content/index.md", "/home/lazlo/StaticSite/template.html", "/home/lazlo/StaticSite/public/index.html")
