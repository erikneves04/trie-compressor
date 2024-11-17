from FileManager.FileManager import FileManager
import pytest # type: ignore
from LZW.Compressor import LZWCompressor
from LZW.Decompressor import LZWDecompressor

# Variáveis de controle
SIGMA_SIZE = 256
DEFAULT_CODE_BITS = 12
INITIAL_BITS_SIZE = 9
CODE_CONTROL_BITS = 32
MAX_DYNAMIC_BITS = 16

def test_compress_and_decompress_do_not_change_the_content():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "Em Algoritmos II, falhar nos testes não é o fim. É apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
    result = compressor.Compress(content)
    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    
    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(code_control_bits, compressed)

    assert content == decompressedContent

def test_compress_and_decompress_empty_string():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = ""
    result = compressor.Compress(content)
    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    
    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(code_control_bits, compressed)

    assert '\x00' == decompressedContent

def test_compressing_and_decompressing_content_with_line_break():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "Em Algoritmos II \n , falhar nos testes não é o fim"
    result = compressor.Compress(content)
    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    
    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(code_control_bits, compressed)

    assert content == decompressedContent

def test_compressing_and_decompressing_only_dots():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "..........."
    result = compressor.Compress(content)
    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    
    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(code_control_bits, compressed)

    assert content == decompressedContent

#def test_compressing_and_decompressing_dynamic_code_lenght_set_right_code_lenght_16_bits():
#    content = FileManager.ReadFile('tests/files/dynamic_input_16_bits.txt')
#    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, MAX_DYNAMIC_BITS, incrementableBits=True)
#    result = compressor.Compress(content)
#    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
#    
#    decompressor = LZWDecompressor(SIGMA_SIZE)
#    decompressedContent = decompressor.Decompress(code_control_bits, compressed)
#
#    assert content == decompressedContent

#def test_compressing_and_decompressing_dynamic_code_lenght_set_right_code_lenght_14_bits():
#    content = FileManager.ReadFile('tests/files/dynamic_input_14_bits.txt')
#    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, MAX_DYNAMIC_BITS, incrementableBits=True)
#    result = compressor.Compress(content)
#    code_control_bits, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
#    
#    decompressor = LZWDecompressor(SIGMA_SIZE)
#    decompressedContent = decompressor.Decompress(code_control_bits, compressed)
#
#    assert content == decompressedContent