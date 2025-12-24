import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", { "href" : "http://localhost/" })
        self.assertEqual(node.to_html(), '<p href="http://localhost/">Hello, world!</p>')
    
    def test_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
