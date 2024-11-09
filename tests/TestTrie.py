import unittest
from src.Trie.Trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
    
    def test_empty_trie_has_zero_nodes(self):
        count = self.trie.GetNodeCount()
        self.assertEqual(count, 0)

    def test_empty_trie_has_depth_one(self):
        depth = self.trie.GetDepth()
        self.assertEqual(depth, 1)

    # TODO: testes de unidade para a Trie