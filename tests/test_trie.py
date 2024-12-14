import pytest
from src.Trie.Trie import Trie

@pytest.fixture(scope="function")
def trie():
    return Trie(detailedReturn = True )

@pytest.fixture(scope="function")
def list_of_insertion():
     return [
        ("01001000", 1),
        ("01100101", 2),
        ("01101100", 3),
        ("01101100", 4),
        ("01101111", 5),
        ("00100000", 6),
        ("01010111", 7),
        ("01101111", 8),
        ("01110010", 9),
        ("01100100", 10),
        ("00100001", 11)
    ]   

@pytest.fixture(scope="function")
def expected_values_insertion():
    return [
        ("01001000", "01001000", None, 1),
        ("01100101", "100101", "001000", 2),
        ("01101100", "1100", "0101", 3),
        ("01101100", "1100", None, 4),
        ("01101111", "11", "00", 5),
        ("00100000", "0100000", "1", 6),
        ("01010111", "10111", "01000", 7),
        ("01101111", "11", None, 8),
        ("01110010", "10010", "0", 9),
        ("01100100", "0", "1", 10),
        ("00100001", "1", "0", 11)
    ]   
    
@pytest.fixture(scope="function")
def expected_values_search():
    return [
        ("01001000", "01000", 1),
        ("01100101", "1", 2),
        ("01101100", "00", 3),
        ("01101100", "00", 3),
        ("01101111", "11", 5),
        ("00100000", "0", 6),
        ("01010111", "10111",7),
        ("01101111", "11", 5),
        ("01110010", "10010", 9),
        ("01100100", "0", 10),
        ("00100001", "1", 11)
    ]

def test_trie_empty_has_zero_nodes(trie):
    assert trie.GetNodeCount() == 1

def test_trie_empty_has_depth_one(trie):
    assert trie.GetDepth() == 1

@pytest.mark.parametrize(
    "key, value, expected", 
    [("000", 1, ("000", "000", None, 1)),
     ("111", 1, ("111", "111", None, 1)),
])
def test_trie_insert_str_bin_trivial_case(trie, key, value, expected):
    result = trie.Insert(key, value)
    assert result == expected

@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected",
    [("000", 1, "111", 2, ("111", "111", None, 2)),
])
def test_trie_insert_two_str_bin_with_different_prefixes(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected
