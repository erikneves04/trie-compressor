import pstats
import os

# Caminho para a pasta "Analysis"
analysis_folder = os.path.dirname(os.path.abspath(__file__))

# Caminhos para os arquivos na pasta "Analysis"
profile_file = os.path.join(analysis_folder, 'profiling_result.prof')
output_file = os.path.join(analysis_folder, 'profiling_analysis.txt')

# Carregar as estatísticas do arquivo
stats = pstats.Stats(profile_file)

# Remover os caminhos completos dos arquivos
stats.strip_dirs()

# Obter o tempo total de execução
total_time = stats.total_tt  # Tempo total de execução registrado

# Salvar os resultados da análise no arquivo de saída
with open(output_file, 'w') as f:
    f.write("10 Funções mais demoradas (tempo acumulado):\n")
    stats.sort_stats('cumulative').stream = f
    stats.print_stats(10)

    f.write("\n10 Funções mais demoradas (tempo total):\n")
    stats.sort_stats('time').stream = f
    stats.print_stats(10)

    f.write("\n10 Funções mais chamadas:\n")
    stats.sort_stats('calls').stream = f
    stats.print_stats(10)

    # Adicionando o tempo total de execução no final
    f.write(f"\nTempo total de execução do programa: {total_time:.6f} segundos\n")

print(f"Tempo total de execução do programa: {total_time:.6f} segundos")
