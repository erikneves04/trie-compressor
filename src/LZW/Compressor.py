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

        prefix = ""
        biggestCode = self.sigmaSize
        #currentBits = self.initialBitsSize
        #maxIntegerForCurrentBits = (2 ** currentBits) - 1
        
        maxCode = (1 << self.initialBitsSize) - 1

        for char in content:
            prefix_with_char = prefix + char

            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(prefix)
            prefix_with_char_key = BinaryConversor.ConvertPrefixToBinaryString(prefix_with_char)

            if self.dict.ContainsKey(prefix_with_char_key):
                prefix = prefix_with_char
            else:
                #value = BinaryConversor.ConvertIntegerToBinaryString(, 12)
                compressedList.append(self.dict[prefix_key])

                #if self.incrementableBits and maxIntegerForCurrentBits == biggestCode:
                #    currentBits += 1
                #    maxIntegerForCurrentBits = (2 ** currentBits) - 1

                # Verificamos se existem bits restantes para o acrescimo de códigos
                if biggestCode < maxCode:
                    self.dict[prefix_with_char_key] = biggestCode
                    biggestCode += 1

                prefix = char
            
        if prefix:
            compressedList.append(self.dict[prefix_key])

        minCodeLenght = biggestCode.bit_length()
        compressedContent = ""

        for code in compressedList:
            converted = BinaryConversor.ConvertIntegerToBinaryString(code, minCodeLenght)
            compressedContent += converted
            
        return compressedContent