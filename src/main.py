import argparse
from enum import Enum
from FileManager.FileManager import FileManager
from LZW import PlotStatistics
from LZW.Compressor import LZWCompressor
from LZW.Decompressor import LZWDecompressor
from LZW.PlotStatistics import PlotStatistics
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
    COMPRESS_FIXED = "compress-fixed"
    COMPRESS_DYNAMIC = "compress-dynamic"
    DECOMPRESS = "decompress"

    def __str__(self):
        return self.value

# Análise de memória
class AnalysisType(Enum):
    NONE = "None"
    CPROGILE = "cProfile"
    MEMRAY = "memray"

    def __str__(self):
        return self.value

def parseArgs():
    parser = argparse.ArgumentParser(description="Aplicação para compressão e descompressão de arquivos - LZW")

    parser.add_argument('--max-code-bits', type=int, required=False, help='Número máximo de bits para os códigos usados.')
    parser.add_argument('--operation', type=Operation, choices=list(Operation), required=True, help='Seleção da operação de compressão ou descompressão.')
    parser.add_argument('--analysis', type=AnalysisType, choices=list(AnalysisType), required=False, default= AnalysisType.NONE, help='Seleção da operação de compressão ou descompressão.')
    parser.add_argument('--statistics', type=bool, required=False, default=False, help='Habilita a geração de estatísticas na compressão e descompresão.')
    parser.add_argument('--origin', type=str, required=True, help='Arquivo de origem.')
    parser.add_argument('--destiny', type=str, required=True, help='Arquivo de destino.')

    return parser.parse_args()

def ExecuteCompressOperation(origin, destiny, initialCodeLengh, maxCodeLenght, dynamic, enableStatistics):
    content = FileManager.ReadFile(origin)
    
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, initialCodeLengh, maxCodeLenght, dynamic, enableStatistics)
    compressedContent = compressor.Compress(content)
    
    FileManager.SaveBinaryFile(destiny, compressedContent)

def ExecuteDecompressOperation(origin, destiny, enableStatistics):
    raw_content = FileManager.ReadBinaryFile(origin)
    maxBitsUsed, content = LZWCompressor.ExtractCodeLenghtAndContent(raw_content, CODE_CONTROL_BITS, enableStatistics)

    decompressor = LZWDecompressor(SIGMA_SIZE)
    decompressedContent = decompressor.Decompress(maxBitsUsed, content)

    FileManager.SaveTextFile(destiny, decompressedContent)

def main():
    args = parseArgs()

    if args.operation == Operation.COMPRESS_FIXED:
        ExecuteCompressOperation(args.origin, args.destiny, DEFAULT_BITS, DEFAULT_BITS, dynamic=False, enableStatistics=args.statistics)
        if args.statistics:
            PlotStatistics.PlotCompression()

    elif args.operation == Operation.COMPRESS_DYNAMIC:
        maxCodeLenght = DEFAULT_BITS if args.max_code_bits == None else args.max_code_bits
        ExecuteCompressOperation(args.origin, args.destiny, DINAMIC_BIT_SIZE_START_WITH, maxCodeLenght, dynamic=True, enableStatistics=args.statistics)
        if args.statistics:
            PlotStatistics.PlotCompression()
        
    elif args.operation == Operation.DECOMPRESS:
        ExecuteDecompressOperation(args.origin, args.destiny, args.statistics)
        if args.statistics:
            PlotStatistics.PlotDecompression()
    
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