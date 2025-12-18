import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("1234BooHoo", TextType.ITALIC)
        self.assertEqual(node.__repr__(), "TextNode(1234BooHoo,TextType.ITALIC,None)")

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a fake node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http://localhost/")
        self.assertNotEqual(node, node2)

    def test_nonedef(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()

