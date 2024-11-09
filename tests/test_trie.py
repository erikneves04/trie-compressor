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

def test_insert_str_bin_trivial_case(trie):
    strInsert = trie.Insert("000", 1)   
    
    assert strInsert[1] == "000" and strInsert[2] == "000" and strInsert[3] == 1
    
def test_insert_two_strings_with_different_prefixes(trie):
    trie.Insert("000", 1)
    strInsertTwo = trie.Insert("111", 2)
    
    assert strInsertTwo[1] == "111" and strInsertTwo[2] == "111" and strInsertTwo[3] == 2
    
def test_insert_two_with_common_prefix(trie):
     trie.Insert("00000", 1)
     strInsertTwo = trie.Insert("00011", 2)
     
     assert strInsertTwo[0] == "2 nós criados"
     assert strInsertTwo[1] == "11"
     assert strInsertTwo[2] == 2
     assert strInsertTwo[3] == "00"
     assert strInsertTwo[4] == 1   
     
       

    