import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
        
    def test_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, node.to_html)

    def test_children_none(self):
        node = ParentNode("foo", None)
        self.assertRaises(ValueError, node.to_html)

    def test_empty_children(self):
        node = ParentNode("foo", [])
        self.assertRaises(ValueError, node.to_html)

    def test_two_children(self):
         child1_node = LeafNode("span", "child1")
         child2_node = LeafNode("span", "child2")
         node = ParentNode("foo", [child1_node, child2_node])
         self.assertEqual(
            node.to_html(),
            "<foo><span>child1</span><span>child2</span></foo>"
            )