import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def GenerateSideBySideForLabel(label, title):
    df = pd.read_csv(f'{label}-statistics.csv')
    sns.set(style="whitegrid", palette="muted")
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    
    sns.lineplot(data=df, x='Time Elapsed (seconds)', y='Compression Rate (%)', ax=axes[0], label='Compression Rate (%)', color='blue')
    sns.lineplot(data=df, x='Time Elapsed (seconds)', y='Progress (%)', ax=axes[0], label='Progress (%)', color='orange')
    axes[0].set_title('Compression Rate and Progress Over Time')
    axes[0].set_xlabel('Time Elapsed (seconds)')
    axes[0].set_ylabel('Percentage (%)')
    axes[0].legend()
    
    sns.lineplot(data=df, x='Time Elapsed (seconds)', y='Dictionary Size (elements)', ax=axes[1], label='Dictionary Size (elements)', color='green')
    axes[1].set_title('Dictionary Size Over Time')
    axes[1].set_xlabel('Time Elapsed (seconds)')
    axes[1].set_ylabel('Dictionary Size (elements)')
    axes[1].legend()
    
    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'Images/{label}_side_by_side.png')
    #plt.show()

def PlotStatistics():
    GenerateSideBySideForLabel('compressed', 'Métricas Coletadas Durante a Compressão')
    GenerateSideBySideForLabel('decompressed', 'Métricas Coletadas Durante a Descompressão')