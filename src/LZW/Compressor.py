from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWCompressor:
    def __init__(self, sigmaSize, initialBitsSize, maxCodeBits, incrementableBits = False):
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.initialBitsSize = initialBitsSize
        self.maxCodeBits = maxCodeBits
        self.incrementableBits = incrementableBits

        # Adicionando os códigos iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = index

    def Compress(self, content):
        compressedList = []

        self.prefix = ""
        self.biggestCode = self.sigmaSize
        #currentBits = self.initialBitsSize
        #maxIntegerForCurrentBits = (2 ** currentBits) - 1
        
        self.maxCode = (1 << self.initialBitsSize) - 1

        for char in content:
            prefix_with_char = self.prefix + char

            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            prefix_with_char_key = BinaryConversor.ConvertPrefixToBinaryString(prefix_with_char)

            if self.dict.ContainsKey(prefix_with_char_key):
                self.prefix = prefix_with_char
            else:
                if self.dict[prefix_key] == None:
                    self.__insertNewCode(prefix_key)

                compressedList.append(self.dict[prefix_key])

                #if self.incrementableBits and maxIntegerForCurrentBits == biggestCode:
                #    currentBits += 1
                #    maxIntegerForCurrentBits = (2 ** currentBits) - 1

                self.__insertNewCode(prefix_with_char_key)
                self.prefix = char
            
        if self.prefix:
            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            compressedList.append(self.dict[prefix_key])

        compressedContent = self.__convertCodesToBinaryString(compressedList)
        
        return compressedContent

    def __insertNewCode(self, prefix_with_char_key):
        if self.biggestCode < self.maxCode:
            self.dict[prefix_with_char_key] = self.biggestCode
            self.biggestCode += 1

    def __convertCodesToBinaryString(self, compressedList):
        minCodeLenght = self.biggestCode.bit_length()
        compressedContent = ""

        for code in compressedList:
            converted = BinaryConversor.ConvertIntegerToBinaryString(code, minCodeLenght)
            compressedContent += converted
            
        return compressedContent