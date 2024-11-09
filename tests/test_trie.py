import pytest
from src.Trie.Trie import Trie 

@pytest.fixture
def trie():
    return Trie()

def test_empty_trie_has_zero_nodes(trie):
    count = trie.GetNodeCount()
    assert count == 1

def test_empty_trie_has_depth_one(trie):
    depth = trie.GetDepth()
    assert depth == 1

# TODO: Add more unit tests for the Trie