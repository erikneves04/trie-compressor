import pytest
from src.Trie.Trie import Trie

@pytest.fixture(scope="function")
def trie():
    return Trie()

@pytest.fixture(scope="function")
def list_of_insertion_and_expected_values():
    return [
        ("01001000", 1, ("01001000", "01001000", None)),
        ("01100101", 2, ("01100101", "100101", "001000")),
        ("01101100", 3, ("01101100", "1100", "0101")),
        ("01101100", 4, ("01101100", "1100", None)),
        ("01101111", 5, ("01101111", "11", "00")),
        ("00100000", 6, ("00100000", "0100000", "1")),
        ("01010111", 7, ("01010111", "10111", "01000")),
        ("01101111", 8, ("01101111", "11", None)),
        ("01110010", 9, ("01110010", "10010", "0")),
        ("01100100", 10, ("01100100", "0", "1")),
        ("00100001", 11, ("00100001", "1", "0"))
    ]   

def test_trie_empty_has_zero_nodes(trie):
    assert trie.GetNodeCount() == 1

def test_trie_empty_has_depth_one(trie):
    assert trie.GetDepth() == 1

@pytest.mark.parametrize(
    "key, value, expected", 
    [("000", 1, ("000", "000", None)),
     ("111", 1, ("111", "111", None)),
])
def test_trie_insert_str_bin_trivial_case(trie, key, value, expected):
    result = trie.Insert(key, value)
    assert result == expected

@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected",
    [("000", 1, "111", 2, ("111", "111", None)),
])
def test_trie_insert_two_str_bin_with_different_prefixes(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected

@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected", 
    [("00000", 1, "00011", 2, ("00011", "11", "00")),
     ("101", 1, "100", 2, ("100", "0", "1")),
     ("110", 1, "111", 2, ("111", "1", "0")),
     ("0110", 1, "0111", 2, ("0111", "1", "0")),
     ("1110", 1, "1111", 2, ("1111", "1", "0")),
     ("00001", 1, "00000", 2, ("00000", "0", "1")),
])
def test_trie_insert_two_str_bin_with_common_prefix(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected
   
@pytest.mark.parametrize(
    "first_key, first_value, second_key, second_value, expected", 
    [("111", 1, "11101", 2, ("11101", "$", "01")),
     ("101", 1, "10111", 2, ("10111", "$", "11")),
     ("110", 1, "11010", 2, ("11010", "$", "10")),
     ("0110", 1, "011011", 2, ("011011", "$", "11")),
     ("000", 1, "0001", 2, ("0001", "$", "1")),
     ("1010", 1, "10101", 2, ("10101", "$", "1")),
     ("1110", 1, "11101", 2, ("11101", "$", "1")),
     ("1001", 1, "100111", 2, ("100111", "$", "11")),
])   
def test_trie_insert_str_bin_into_leaf_node(trie, first_key, first_value, second_key, second_value, expected):
    trie.Insert(first_key, first_value)
    result = trie.Insert(second_key, second_value)
    assert result == expected

def test_trie_insert_random_list_str_bin(trie, list_of_insertion_and_expected_values):
    for key, value, expected in list_of_insertion_and_expected_values:
        result = trie.Insert(key, value)
        assert result == expected

    assert trie.GetNodeCount() == 18
    
def test_trie_insert_string_void(trie):
    with pytest.raises(ValueError):
        trie.Insert("", 1)  

def test_trie_insert_value_not_int(trie):
    with pytest.raises(ValueError):
        trie.Insert("0101", "string") 

def test_trie_insert_value_not_positive(trie):
    with pytest.raises(ValueError):
        trie.Insert("0101", -1)  

    with pytest.raises(ValueError):
        trie.Insert("0101", 0)  


