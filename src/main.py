import argparse
from enum import Enum
from LZW.Compressor import LZWCompressor
from FileManager.FileManager import FileManager

# Constantes
SIGMA_SIZE = 256                # Tamanho do alfabeto utilizado
DEFAULT_BITS = 12               # Tamanho padrão dos códigos
DINAMIC_BIT_SIZE_START_WITH = 9 # Tamanho inicial dos códigos no caso de número incrementável de bits

# Operações disponíveis
class Operation(Enum):
    COMPRESS_FIXED = "compress-fixed"
    COMPRESS_DYNAMIC = "compress-dynamic"
    DECOMPRESS = "decompress"

    def __str__(self):
        return self.value

def parseArgs():
    parser = argparse.ArgumentParser(description="Aplicação para compressão e descompressão de arquivos - LZW")

    parser.add_argument('--max-code-bits', type=int, required=False, help='Número máximo de bits para os códigos usados.')
    parser.add_argument('--operation', type=Operation, choices=list(Operation), required=True, help='Seleção da operação de compressão ou descompressão.')
    parser.add_argument('--origin', type=str, required=True, help='Arquivo de origem.')
    parser.add_argument('--destiny', type=str, required=True, help='Arquivo de destino.')
    
    return parser.parse_args()

def ExecuteCompressOperation(origin, destiny, initialCodeLengh, maxCodeLenght, dynamic):
    content = FileManager.ReadFile(origin)
    
    compressor = LZWCompressor(SIGMA_SIZE, initialCodeLengh, maxCodeLenght, dynamic)
    compressedContent = compressor.Compress(content)
    
    FileManager.SaveBinaryFile(destiny, compressedContent)

def ExecuteDecompressOperation(origin, destiny, maxBits):
    content = FileManager.ReadFile(origin)
    pass

def main():
    args = parseArgs()

    if args.operation == Operation.COMPRESS_FIXED:
        ExecuteCompressOperation(args.origin, args.destiny, DEFAULT_BITS, DEFAULT_BITS, dynamic=False)

    elif args.operation == Operation.COMPRESS_DYNAMIC:
        maxCodeLenght = DEFAULT_BITS if args.max_code_bits == None else args.max_code_bits
        ExecuteCompressOperation(args.origin, args.destiny, DINAMIC_BIT_SIZE_START_WITH, maxCodeLenght, dynamic=True)

    elif args.operation == Operation.DECOMPRESS:
        ExecuteDecompressOperation(args.origin, args.destiny, args.max_code_bits)

    else:
        print ("Invalid operation selected.")
        exit (1)

if __name__ == "__main__":
    main()