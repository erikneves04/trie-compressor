import time
import psutil
import pandas as pd
from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWCompressor:
    def __init__(self, sigmaSize, controlBits, initialBitsSize, maxCodeBits, incrementableBits=False, log_metrics=False):
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.controlBits = controlBits
        self.initialBitsSize = initialBitsSize
        self.maxCodeBits = maxCodeBits
        self.incrementableBits = incrementableBits
        self.log_metrics = log_metrics

        # Inicializando o dicionário com as raízes iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = index

        # Inicializando as métricas
        self.start_time = None
        self.end_time = None
        self.original_size = 0
        self.compressed_size = 0
        self.dictionnary_size = 0
        self.memory_usage = 0
        self.metrics_log = []

    def Compress(self, content):
        self.start_time = time.time()  # Inicia o tempo de execução
        self.original_size = len(content)
        
        compressedList = []
        self.prefix = ""
        self.biggestCode = self.sigmaSize
        self.currentBits = self.initialBitsSize
        self.maxCode = (1 << self.currentBits) - 1
        
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

            # Atualiza as estatísticas a cada 5% da execução
            #if i % (len(content) // 5) == 0:
            #    self.update_statistics(i, len(content))

        if self.prefix:
            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            compressedList.append(self.dict[prefix_key])

        #self.end_time = time.time()  # Fim do tempo de execução
        #self.compressed_size = len(compressedList)
        #self.update_statistics(len(content), len(content))

        #self.save_metrics_to_csv()

        return self.__convertCodesToBinaryString(compressedList)

    def update_statistics(self, processed, total):
        compression_rate = (self.original_size - self.compressed_size) / self.original_size * 100
        self.dictionnary_size = self.dict.GetNodeCount()
        process = psutil.Process()
        self.memory_usage = process.memory_info().rss
        progress = (processed / total) * 100

        metric_data = {
            'Progress (%)': progress,
            'Compression Rate (%)': compression_rate,
            'Dictionary Size (elements)': self.dictionnary_size,
            'Memory Usage (bytes)': self.memory_usage,
            'Compressed Size (bytes)': self.compressed_size,
            'Time Elapsed (seconds)': time.time() - self.start_time
        }
        self.metrics_log.append(metric_data)

    def save_metrics_to_csv(self):
        df = pd.DataFrame(self.metrics_log)
        df.to_csv('compression-logs.csv', index=False)

    def __insertNewCode(self, prefix_with_char_key):
        if self.biggestCode == self.maxCode:
            self.__incrementCurrentCodeBits()

        if self.biggestCode < self.maxCode:
            self.dict[prefix_with_char_key] = self.biggestCode
            self.biggestCode += 1

    def __incrementCurrentCodeBits(self):
        if self.incrementableBits and self.currentBits < self.maxCodeBits:
            self.currentBits += 1
            self.maxCode = (1 << self.currentBits) - 1

    def __convertCodesToBinaryString(self, compressedList):
        minCodeLength = self.biggestCode.bit_length()
        controlString = BinaryConversor.ConvertIntegerToBinaryString(minCodeLength, self.controlBits)

        compressedContent = [controlString]

        for code in compressedList:
            converted = BinaryConversor.ConvertIntegerToBinaryString(code, minCodeLength)
            compressedContent.append(converted)

        return ''.join(compressedContent)

    @staticmethod
    def ExtractCodeLenghtAndContent(input, controlBits):
        code_length_bits = input[:controlBits]
        code_length = int(code_length_bits, 2)
        content = input[controlBits:]
        return code_length, content