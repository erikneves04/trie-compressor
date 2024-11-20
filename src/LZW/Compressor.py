import pandas as pd
from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie
import time

class LZWCompressor:
    """
    Classe responsável pela compressão de dados usando o algoritmo LZW (Lempel-Ziv-Welch).
    """

    def __init__(self, sigmaSize, controlBits, initialBitsSize, maxCodeBits, incrementableBits=False, enableStatistics=False):
        """
        Inicializa o compressor LZW com os parâmetros fornecidos.

        :param sigmaSize: Tamanho do alfabeto.
        :param controlBits: Bits de controle para a compressão.
        :param initialBitsSize: Tamanho inicial dos bits.
        :param maxCodeBits: Tamanho máximo dos códigos.
        :param incrementableBits: Indica se os bits podem ser incrementados.
        :param enableStatistics: Habilita a coleta de estatísticas.
        """
        
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.controlBits = controlBits
        self.initialBitsSize = initialBitsSize
        self.maxCodeBits = maxCodeBits
        self.incrementableBits = incrementableBits
        
        self.enableStatistics = enableStatistics
        self.statistics = []
        self.startTime = time.time()

        # Inicializando o dicionário com as raízes iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = index            

    def Compress(self, content):        
        """
        Comprime o conteúdo fornecido usando o algoritmo LZW.

        :param content: Dados a serem comprimidos.
        :return: String binária representando o conteúdo comprimido.
        """
        
        compressedList = []

        self.prefix = ""
        self.biggestCode = self.sigmaSize
        self.currentBits = self.initialBitsSize
        self.maxCode = (1 << self.currentBits) - 1

        self.__registerStatistics(content, compressedList, len(content))

        for i, char in enumerate(content):
            prefix_with_char = ''.join(self.prefix) + char
            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(''.join(self.prefix))
            prefix_with_char_key = prefix_key + BinaryConversor.ConvertIntegerToBinaryString(ord(char))

            dictValue = self.dict[prefix_with_char_key]
            if dictValue is not None:
                self.prefix = prefix_with_char
            else:
                prefixValue = self.dict[prefix_key]
                if self.dict[prefix_key] is None:
                    self.__insertNewCode(prefix_key)
                    prefixValue = self.dict[prefix_key]

                value = prefixValue
                compressedList.append(value)

                self.__insertNewCode(prefix_with_char_key)
                self.prefix = char

            self.__registerStatistics(content, compressedList, i)

        if self.prefix:
            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            compressedList.append(self.dict[prefix_key])
            self.__registerStatistics(content, compressedList, len(content), last=True)

        self.__saveStatistics()

        return self.__convertCodesToBinaryString(compressedList)

    def __saveStatistics(self):
        """
        Salva as estatísticas de compressão em um arquivo CSV, se habilitado.
        """
        
        if self.enableStatistics:
            df = pd.DataFrame(self.statistics)
            df.to_csv('compressed-statistics.csv', index=False)

    def __registerStatistics(self, content, compressedList, i, last = False):
        """
        Registra as estatísticas de compressão em diferentes pontos do processo.

        :param content: Conteúdo original.
        :param compressedList: Lista de códigos comprimidos.
        :param i: Índice atual do processamento.
        :param last: Flag para indicar se é o último ponto de compressão.
        """
        
        if not self.enableStatistics:
            return
        
        if (not last) and not (i % (len(content) // 20) == 0):
            return

        compressionRate = ((len(compressedList) * self.currentBits) / ((i + 1) * 8)) * 100
        timeElapsed = time.time() - self.startTime
        dictSize = self.dict.GetNodeCount()
        progress = (i / len(content)) * 100
        
        self.statistics.append(
            {
                'Progress (%)': progress,
                'Compression Rate (%)': compressionRate,
                'Dictionary Size (elements)': dictSize,
                'Time Elapsed (seconds)': timeElapsed
            })            

    def __insertNewCode(self, prefix_with_char_key):
        """
        Insere um novo código no dicionário LZW.

        :param prefix_with_char_key: A chave do prefixo e caractere a ser inserido.
        """
        
        if self.biggestCode == self.maxCode:
            self.__incrementCurrentCodeBits()

        if self.biggestCode < self.maxCode:
            self.dict[prefix_with_char_key] = self.biggestCode
            self.biggestCode += 1

    def __incrementCurrentCodeBits(self):
        """
        Incrementa o número de bits usados para os códigos, se permitido.
        """

        if self.incrementableBits and self.currentBits < self.maxCodeBits:
            self.currentBits += 1
            self.maxCode = (1 << self.currentBits) - 1

    def __convertCodesToBinaryString(self, compressedList):
        """
        Converte a lista de códigos comprimidos para uma string binária.

        :param compressedList: Lista de códigos comprimidos.
        :return: String binária representando os códigos comprimidos.
        """

        minCodeLength = self.biggestCode.bit_length()
        controlString = BinaryConversor.ConvertIntegerToBinaryString(minCodeLength, self.controlBits)

        compressedContent = [controlString]

        for code in compressedList:
            converted = BinaryConversor.ConvertIntegerToBinaryString(code, minCodeLength)
            compressedContent.append(converted)

        return ''.join(compressedContent)

    @staticmethod
    def ExtractCodeLenghtAndContent(input, controlBits):
        """
        Extrai o comprimento do código e o conteúdo a partir da string binária de entrada.

        :param input: String binária de entrada.
        :param controlBits: Número de bits de controle.
        :return: Comprimento do código e conteúdo restante.
        """

        code_length_bits = input[:controlBits]
        code_length = int(code_length_bits, 2)
        content = input[controlBits:]
        return code_length, content