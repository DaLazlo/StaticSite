import unittest

from block import BlockType, block_to_block_type

class TestBlock(unittest.TestCase):
    def test_block_to_type_ordered(self):
        a_block = '''1. foo
2. bar
3. baz'''
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(a_block))

    def test_block_to_type_heading(self):
        a_block = '''### foo'''
        self.assertEqual(BlockType.HEADING, block_to_block_type(a_block))

    def test_block_to_type_code(self):
        a_block = '''```some code
        more code```'''
        self.assertEqual(BlockType.CODE, block_to_block_type(a_block))

    def test_block_to_type_unordered(self):
        a_block = '''- foo
        - bar
        -baz'''
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(a_block))

    def test_block_to_type_paragraph(self):
        a_block = '''some boring text
        as an example'''
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(a_block))