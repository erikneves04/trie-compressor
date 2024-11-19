import pandas as pd
from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie
import time

class LZWCompressor:
    def __init__(self, sigmaSize, controlBits, initialBitsSize, maxCodeBits, incrementableBits=False, enableStatistics=False):
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
        if self.enableStatistics:
            df = pd.DataFrame(self.statistics)
            df.to_csv('compressed-statistics.csv', index=False)

    def __registerStatistics(self, content, compressedList, i, last = False):
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
                #'Memory Usage (bytes)': memory_usage,
                'Time Elapsed (seconds)': timeElapsed
            })            

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