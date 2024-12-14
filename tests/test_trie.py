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

@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected", 
    [("00000", 1, "00011", 2, ("00011", "11", "00", 2)),
     ("101", 1, "100", 2, ("100", "0", "1", 2)),
     ("110", 1, "111", 2, ("111", "1", "0", 2)),
     ("0110", 1, "0111", 2, ("0111", "1", "0", 2)),
     ("1110", 1, "1111", 2, ("1111", "1", "0", 2)),
     ("00001", 1, "00000", 2, ("00000", "0", "1", 2)),
])
def test_trie_insert_two_str_bin_with_common_prefix(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected
   
@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected", 
    [("111", 1, "11101", 2, ("11101", "$", "01", 2)),
     ("101", 1, "10111", 2, ("10111", "$", "11", 2)),
     ("110", 1, "11010", 2, ("11010", "$", "10", 2)),
     ("0110", 1, "011011", 2, ("011011", "$", "11", 2)),
     ("000", 1, "0001", 2, ("0001", "$", "1", 2)),
     ("1010", 1, "10101", 2, ("10101", "$", "1", 2)),
     ("1110", 1, "11101", 2, ("11101", "$", "1", 2)),
     ("1001", 1, "100111", 2, ("100111", "$", "11", 2))
])   
def test_trie_insert_str_bin_into_leaf_node(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected

def test_trie_insert_random_list_str_bin(trie, list_of_insertion, expected_values_insertion):
    for (key, value), expected in zip(list_of_insertion, expected_values_insertion):
        result = trie.Insert(key, value)
        assert result == expected

    assert trie.GetNodeCount() == 20
        
def test_trie_split_intermediate_node_leaf(trie):
    trie.Insert("111",1)
    trie.Insert("1110",2)
    result = trie.Insert("110",3)
    assert result == ("110", "0", "1", 3) 
