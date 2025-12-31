from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(a_block):
    if re.match(r"^#{1,6} .*", a_block):
        return BlockType.HEADING
    elif re.match(r"^```.+```$", a_block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"(^>[^>]*)+", a_block, re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(r"(^- (.+))+", a_block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif list(range(1,len(a_block.split("\n"))+1)) == list(map(int, re.findall(r"^(\d{1,2})\. ", a_block, re.MULTILINE))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH