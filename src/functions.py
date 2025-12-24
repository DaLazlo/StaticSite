from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, { "href":text_node.url })
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, { "src":text_node.url, "alt":text_node.text })
    else:
        raise Exception("unknown type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            #raise Exception("delimiter not present")
            new_nodes.append(node)
        else:
            pre, inner, post = node.text.split(delimiter)
            new_nodes.extend([ TextNode(pre, TextType.TEXT), TextNode(inner, text_type), TextNode(post, TextType.TEXT)])
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^[]*)\]\(([^(]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[([^[]*)\]\(([^(]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
        else:
            text = node.text
            for image in images:
                parts = text.split(f"![{image[0]}]({image[1]})", 1)
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text = parts[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
        else:
            text = node.text
            for link in links:
                first, text = text.split(f"[{link[0]}]({link[1]})")
                new_nodes.append(TextNode(first, TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
                    split_nodes_image(
                        split_nodes_delimiter(
                            split_nodes_delimiter(
                                split_nodes_delimiter([node], "`", TextType.CODE),
                            "**", TextType.BOLD),
                        "_", TextType.ITALIC)))