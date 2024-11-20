import time

import pandas as pd
from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWDecompressor:
    """
    Classe responsável pela descompressão de dados utilizando o algoritmo LZW (Lempel-Ziv-Welch).

    """

    def __init__(self, sigmaSize, enableStatistics=False):
        """
        Inicializa o descompressor LZW com os parâmetros fornecidos.

        :param sigmaSize: Tamanho do alfabeto.
        :param enableStatistics: Habilita a coleta de estatísticas.
        """
        
        self.dict = Trie()
        self.sigmaSize = sigmaSize

        # Inicializando o dicionário com as raízes iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = chr(index)

        self.enableStatistics = enableStatistics
        self.statistics = []
        self.startTime = time.time()

    def Decompress(self, code_length, content):
        """
        Descomprime o conteúdo fornecido utilizando o algoritmo LZW.

        :param code_length: Comprimento do código de cada símbolo comprimido.
        :param content: Dados comprimidos a serem descomprimidos.
        :return: String descomprimida.
        """
        
        decompressedList = []

        biggestCode = self.sigmaSize

        current = self.__getNextCode(content, 0, code_length)
        currentString = self.dict[current]
        decompressedList.append(currentString)
        
        index = code_length
        contentLen = len(content)

        while index < contentLen:
            previous = current
            previousString = currentString

            current = self.__getNextCode(content, index, code_length)
            index += code_length

            dictValue = self.dict[current]
            if dictValue != None:
                currentString = dictValue
                decompressedList.append(currentString)

                P = previousString
                C = currentString[0]

                self.dict[BinaryConversor.ConvertIntegerToBinaryString(biggestCode)] = P + C
                biggestCode += 1

            else:
                P = previousString
                C = P[0]

                currentString = P + C
                decompressedList.append(currentString)

                self.dict[BinaryConversor.ConvertIntegerToBinaryString(biggestCode)] = currentString
                biggestCode += 1
            
            self.__registerStatistics(content, decompressedList, index, code_length)
        
        self.__saveStatistics()

        return ''.join(decompressedList)

    def __saveStatistics(self):
        """
        Salva as estatísticas de descompressão em um arquivo CSV, se habilitado.
        """

        if self.enableStatistics:
            df = pd.DataFrame(self.statistics)
            df.to_csv('decompressed-statistics.csv', index=False)

    def __registerStatistics(self, compressedList, decompressedList, currentIndex, codeBits, last=False):
        """
        Registra as estatísticas de descompressão em diferentes pontos do processo.

        :param compressedList: Lista de códigos comprimidos.
        :param decompressedList: Lista de códigos descomprimidos.
        :param currentIndex: Índice atual do processamento.
        :param codeBits: Tamanho do código em bits.
        :param last: Flag para indicar se é o último ponto de descompressão.
        """
        
        if not self.enableStatistics:
            return

        if (not last) and not (len(decompressedList) * codeBits % (len(compressedList) // 128) == 0):
            return

        decompressedSize = len(decompressedList)
        decompressionRate = (decompressedSize*8 / len(compressedList)) * 100

        progress = ((currentIndex) / len(compressedList)) * 100 if len(compressedList) > 0 else 0
        timeElapsed = time.time() - self.startTime
        dictSize = self.dict.GetNodeCount()

        self.statistics.append(
            {
                'Progress (%)': progress,
                'Compression Rate (%)': decompressionRate,
                'Dictionary Size (elements)': dictSize,
                'Time Elapsed (seconds)': timeElapsed
            }
        )

    def __getNextCode(self, content, index, code_length):
        """
        Extrai o próximo código a partir do conteúdo comprimido.

        :param content: Dados comprimidos.
        :param index: Índice atual para ler o código.
        :param code_length: Comprimento do código em bits.
        :return: O próximo código extraído.
        """
        
        code_bits = content[index:index + code_length]
        return code_bits.lstrip('0') or '0'
