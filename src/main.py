import argparse
from enum import Enum
from FileManager.FileManager import FileManager
from LZW.Compressor import LZWCompressor
from LZW.Decompressor import LZWDecompressor
import cProfile
import subprocess
import os
import memray
from memray import FileDestination

# Constantes
SIGMA_SIZE = 256                # Tamanho do alfabeto utilizado
DEFAULT_BITS = 12               # Tamanho padrão dos códigos
DINAMIC_BIT_SIZE_START_WITH = 9 # Tamanho inicial dos códigos no caso de número incrementável de bits
CODE_CONTROL_BITS = 32          # Tamanho da código de controle incluido no começo do arquivo comprimido, usado na descompressão

# Operações disponíveis
class Operation(Enum):
    """
    Enumeração de operações disponíveis para compressão e descompressão.

    COMPRESS_FIXED: Compressão com um número fixo de bits.
    COMPRESS_DYNAMIC: Compressão com um número dinâmico de bits.
    DECOMPRESS: Descompressão.
    """
    COMPRESS_FIXED = "compress-fixed"
    COMPRESS_DYNAMIC = "compress-dynamic"
    DECOMPRESS = "decompress"

    def __str__(self):
        return self.value

# Análise de memória
class AnalysisType(Enum):
    """
    Enumeração para definir o tipo de análise de desempenho a ser realizada.

    NONE: Nenhuma análise de desempenho.
    CPROGILE: Análise utilizando cProfile.
    MEMRAY: Análise utilizando Memray.
    """
    NONE = "None"
    CPROGILE = "cProfile"
    MEMRAY = "memray"

    def __str__(self):
        return self.value

def parseArgs():
    """
    Função para fazer o parsing dos argumentos da linha de comando.

    :return: Retorna um objeto com os argumentos parseados.
    """
    parser = argparse.ArgumentParser(description="Aplicação para compressão e descompressão de arquivos - LZW")

    parser.add_argument('--max-code-bits', type=int, required=False, help='Número máximo de bits para os códigos usados.')
    parser.add_argument('--operation', type=Operation, choices=list(Operation), required=True, help='Seleção da operação de compressão ou descompressão.')
    parser.add_argument('--analysis', type=AnalysisType, choices=list(AnalysisType), required=False, default= AnalysisType.NONE, help='Seleção da operação de compressão ou descompressão.')
    parser.add_argument('--statistics', type=bool, required=False, default=False, help='Habilita a geração de estatísticas na compressão e descompresão.')
    parser.add_argument('--origin', type=str, required=True, help='Arquivo de origem.')
    parser.add_argument('--destiny', type=str, required=True, help='Arquivo de destino.')

    return parser.parse_args()

def ExecuteCompressOperation(origin, destiny, initialCodeLengh, maxCodeLenght, dynamic):
    """
    Função responsável por executar a compressão de um arquivo.

    :param origin: Caminho do arquivo de origem a ser comprimido.
    :param destiny: Caminho do arquivo de destino para armazenar o conteúdo comprimido.
    :param initialCodeLengh: Comprimento inicial do código a ser usado para compressão.
    :param maxCodeLenght: Comprimento máximo dos códigos para a compressão.
    :param dynamic: Se a compressão será feita com tamanho de código dinâmico (True) ou fixo (False).
    """
    content = FileManager.ReadFile(origin)
    
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, initialCodeLengh, maxCodeLenght, dynamic)
    compressedContent = compressor.Compress(content)
    
    FileManager.SaveBinaryFile(destiny, compressedContent)

def ExecuteDecompressOperation(origin, destiny):
    """
    Função responsável por executar a descompressão de um arquivo.

    :param origin: Caminho do arquivo de origem a ser descomprimido.
    :param destiny: Caminho do arquivo de destino para armazenar o conteúdo descomprimido.
    """
    raw_content = FileManager.ReadBinaryFile(origin)
    maxBitsUsed, content = LZWCompressor.ExtractCodeLenghtAndContent(raw_content, CODE_CONTROL_BITS)

    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(maxBitsUsed, content)

    FileManager.SaveTextFile(destiny, decompressedContent)

def main():
    """
    Função principal do programa. Executa a operação selecionada (compressão ou descompressão) com base nos argumentos fornecidos.

    - Compressão: Executa a compressão de arquivos com o número fixo ou dinâmico de bits.
    - Descompressão: Executa a descompressão de arquivos.
    """
    args = parseArgs()

    if args.operation == Operation.COMPRESS_FIXED:
        ExecuteCompressOperation(args.origin, args.destiny, DEFAULT_BITS, DEFAULT_BITS, dynamic=False,)

    elif args.operation == Operation.COMPRESS_DYNAMIC:
        maxCodeLenght = DEFAULT_BITS if args.max_code_bits == None else args.max_code_bits
        ExecuteCompressOperation(args.origin, args.destiny, DINAMIC_BIT_SIZE_START_WITH, maxCodeLenght, dynamic=True)

    elif args.operation == Operation.DECOMPRESS:
        ExecuteDecompressOperation(args.origin, args.destiny)

    else:
        print("Invalid operation selected.")
        exit(1)

if __name__ == "__main__":
    args = parseArgs()
    
    if args.analysis == AnalysisType.CPROGILE:
        analysis_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Analysis")

        if not os.path.exists(analysis_folder):
            os.makedirs(analysis_folder)
        
        # Caminho completo para o arquivo de saída do cProfile
        profile_output_file = os.path.join(analysis_folder, "profiling_result.prof")
        
        # Executa o perfil e salva na pasta "Analysis"
        cProfile.run('main()', profile_output_file)
        
        # Executa o script de análise do perfil, que também estará na pasta "Analysis"
        subprocess.run(["python3", os.path.join(analysis_folder, "analyze_profile.py")])
    elif args.analysis == AnalysisType.MEMRAY:
        # Caminho para a pasta "Analysis" no mesmo nível da pasta "src"
        analysis_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Analysis")

        # Verifica se a pasta "Analysis" existe, se não, cria
        if not os.path.exists(analysis_folder):
            os.makedirs(analysis_folder)
            
        memray_output_file = os.path.join(analysis_folder, "memray_output.bin")
        if os.path.exists(memray_output_file):
            os.remove(memray_output_file)
        with memray.Tracker(destination=FileDestination(memray_output_file)) as tracker:
            # Executa a lógica principal do código com profiling de memória
            main()

    else:
        main()