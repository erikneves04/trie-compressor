from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWCompressor:
    def __init__(self, sigmaSize, codeBits, initialBitsSize, incrementableBits = False):
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.codeBits = codeBits
        self.initialBitsSize = initialBitsSize
        self.incrementableBits = incrementableBits

        # Adicionando os códigos iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = index

    def Compress(self, content):
        compressedcontent = []

        prefix = ""
        biggestCode = self.sigmaSize
        #currentBits = self.initialBitsSize
        #maxIntegerForCurrentBits = (2 ** currentBits) - 1
        
        for char in content:
            prefix_with_char = prefix + char

            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(prefix)
            prefix_with_char_key = BinaryConversor.ConvertPrefixToBinaryString(prefix_with_char)

            if self.dict.ContainsKey(prefix_with_char_key):
                prefix = prefix_with_char
            else:
                value = BinaryConversor.ConvertIntegerToBinaryString(self.dict[prefix_key], 12)
                compressedcontent.append(value)

                #if self.incrementableBits and maxIntegerForCurrentBits == biggestCode:
                #    currentBits += 1
                #    maxIntegerForCurrentBits = (2 ** currentBits) - 1

                self.dict[prefix_with_char_key] = biggestCode
                biggestCode += 1

                prefix = char
            
        if prefix:
            value = BinaryConversor.ConvertIntegerToBinaryString(self.dict[prefix_key], 12)
            compressedcontent.append(value)

        return ''.join(compressedcontent)