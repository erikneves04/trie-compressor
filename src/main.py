import argparse
from enum import Enum
from LZW.Compressor import LZWCompressor
from FileManager.FileManager import FileManager

# Constantes
SIGMA_SIZE = 2    # Tamanho do alfabeto utilizado
DEFAULT_BITS = 12 # Tamanho padrão dos códigos

# Operações disponíveis
class Operation(Enum):
    COMPRESS = "compress"
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

def ExecuteCompressOperation(origin, destiny, maxBits):
    content = FileManager.ReadFileAsBinary(origin)
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_BITS)

    compressor.Compress(content)

def ExecuteDecompressOperation(origin, destiny, maxBits):
    content = FileManager.ReadFileAsText(origin)
    pass

def main():
    args = parseArgs()

    if args.operation == Operation.COMPRESS:
        ExecuteCompressOperation(args.origin, args.destiny, args.max_code_bits)
    elif args.operation == Operation.DECOMPRESS:
        ExecuteDecompressOperation(args.origin, args.destiny, args.max_code_bits)
    else:
        print ("Invalid operation selected.")
        exit (1)

if __name__ == "__main__":
    main()