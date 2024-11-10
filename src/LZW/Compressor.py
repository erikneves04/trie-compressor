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
            self.dict.Insert(str(index), index)

    def __convertIntegerToBinaryString(self, integer, size):
        binary_str = bin(integer)[2:]
        return binary_str.zfill(size)

    def Compress(self, content):
        compressedcontent = ""

        prefix = ''
        biggestCode = self.sigmaSize - 1

        for char in content:
            prefix_with_char = prefix + char
            
            if self.dict.ContainsKey(prefix_with_char):
                prefix = prefix_with_char
            else:
                compressedcontent += ' ' + self.__convertIntegerToBinaryString(self.dict[prefix], 12)

                biggestCode += 1
                self.dict[prefix_with_char] = biggestCode

                prefix = char

        if prefix:
            compressedcontent += ' ' + self.__convertIntegerToBinaryString(self.dict[prefix], 12)

        return compressedcontent.strip()
        