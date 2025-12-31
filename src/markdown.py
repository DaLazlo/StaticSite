
from block import BlockType, block_to_block_type
from functions import markdown_to_blocks, text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

import re

def markdown_to_html_node(markdown):
    my_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        mytype = block_to_block_type(block)
        if mytype == BlockType.HEADING:
            mynum, mytext = re.findall(r"^(#{1,6}) (.*)", block)[0]
            children = text_to_children(mytext)
            my_nodes.append(ParentNode(f"h{len(mynum)}", children, None))
        elif mytype == BlockType.QUOTE:
            mytext = re.findall(r"^> ([^>]+)", block, re.MULTILINE)[0]
            children = text_to_children(mytext)
            my_nodes.append(ParentNode("blockquote", children, None))
        elif mytype == BlockType.UNORDERED_LIST:
            listitems = re.findall(r"^- (.+)+", block, re.MULTILINE)
            items = []
            for item in listitems:
                children = text_to_children(item)
                items.append(ParentNode("li", children, None))
            my_nodes.append(ParentNode("ul", items, None))
        elif mytype == BlockType.ORDERED_LIST:
            listitems = re.findall(r"^\d{1,2}\. (.+)", block, re.MULTILINE)
            items = []
            for item in listitems:
                children = text_to_children(item)
                items.append(ParentNode("li", children, None))
            my_nodes.append(ParentNode("ol", items, None))
        elif mytype == BlockType.CODE:
            mytext = re.findall(r"^```(.+)```$", block, re.MULTILINE|re.DOTALL)[0]
            my_nodes.append(ParentNode("pre", [ text_node_to_html_node(TextNode(mytext.lstrip(), TextType.CODE)) ], None))
        elif mytype == BlockType.PARAGRAPH:
            my_nodes.append(ParentNode("p", text_to_children(block.strip()), None))
    
    return ParentNode("div", my_nodes, None)

def text_to_children(text):
    my_text_node = text_to_textnodes(text)
    my_html_nodes = []
    for node in my_text_node:
        my_html_nodes.append(text_node_to_html_node(node))
    return my_html_nodes

def extract_title(markdown):
    title = re.findall(r"^# (.+)", markdown, re.MULTILINE)
    try:
        return title[0]
    except:
        raise Exception("no title found")
       

            