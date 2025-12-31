import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from functions import *

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "http://localhost/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, { "href":"http://localhost/"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "http://localhost/image.img")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, { "src":"http://localhost/image.img", "alt":"This is a text node" })

    def test_error(self):
        node = TextNode("This is a text node", "FOO")
        self.assertRaises(Exception, text_node_to_html_node, node)
    
    # tests for split_nodes_delimiter

    def test_split_italic(self):
        node = TextNode("this is an _italic_ test", TextType.TEXT)
        [ pre, inner, post ] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(pre, TextNode("this is an ", TextType.TEXT))
        self.assertEqual(inner, TextNode("italic", TextType.ITALIC))
        self.assertEqual(post, TextNode(" test", TextType.TEXT))

    def test_split_italic_twice(self):
        node = TextNode("this is an _italic_ test", TextType.TEXT)
        node2 = TextNode("this is also an _italic_ test", TextType.TEXT)
        [ pre1, inner1, post1, pre2, inner2, post2 ] = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        self.assertEqual(pre1, TextNode("this is an ", TextType.TEXT))
        self.assertEqual(inner1, TextNode("italic", TextType.ITALIC))
        self.assertEqual(post1, TextNode(" test", TextType.TEXT))
        self.assertEqual(pre2, TextNode("this is also an ", TextType.TEXT))
        self.assertEqual(inner2, TextNode("italic", TextType.ITALIC))
        self.assertEqual(post2, TextNode(" test", TextType.TEXT))

    def test_split_code(self):
        node = TextNode("this is a `code` test", TextType.TEXT)
        [ pre, inner, post ] = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(pre, TextNode("this is a ", TextType.TEXT))
        self.assertEqual(inner, TextNode("code", TextType.CODE))
        self.assertEqual(post, TextNode(" test", TextType.TEXT))

    def test_split_bold(self):
        node = TextNode("this is a **bold** test", TextType.TEXT)
        [ pre, inner, post ] = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(pre, TextNode("this is a ", TextType.TEXT))
        self.assertEqual(inner, TextNode("bold", TextType.BOLD))
        self.assertEqual(post, TextNode(" test", TextType.TEXT))
    
    def test_split_pass(self):
        node = TextNode("this is bold", TextType.BOLD)
        [ newnode ] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(newnode, node)

    def test_split_error(self):
        node = TextNode("this is text", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, node, "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [sometext](https://localhost/foo)"
            )
        self.assertListEqual([("sometext", "https://localhost/foo")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
            )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with an [a link](http://localhost/) and another [link 2](https://localhost/)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "http://localhost/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link 2", TextType.LINK, "https://localhost/"
                ),
            ],
            new_nodes,
            )
        
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertEqual(text_to_textnodes(text), output)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )