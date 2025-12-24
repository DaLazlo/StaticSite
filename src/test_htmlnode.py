import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("fake", "text which is purported to be fake", None, {"href":"https://localhost/"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("fake", "text which is purported to be fake", None, {"href":"https://localhost/"})
        self.assertEqual(node.props_to_html(), ' href="https://localhost/"')

    def test_print(self):
        node = HTMLNode("fake", "text which is purported to be fake", None, {"href":"https://localhost/"})
        self.assertEqual(node.__repr__(), 'fake : text which is purported to be fake : None : href="https://localhost/"')

if __name__ == "__main__":
    unittest.main()
