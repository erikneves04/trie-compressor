from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWCompressor:
    def __init__(self, sigmaSize, controlBits, initialBitsSize, maxCodeBits, incrementableBits = False):
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.controlBits = controlBits
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

        self.currentBits = self.initialBitsSize
        self.maxCode = (1 << self.currentBits) - 1

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

                self.__insertNewCode(prefix_with_char_key)
                self.prefix = char
            
        if self.prefix:
            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            compressedList.append(self.dict[prefix_key])
        
        return self.__convertCodesToBinaryString(compressedList)

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
        minCodeLenght = self.biggestCode.bit_length()
        controlString = BinaryConversor.ConvertIntegerToBinaryString(minCodeLenght, self.controlBits)
        
        compressedContent = controlString

        for code in compressedList:
            converted = BinaryConversor.ConvertIntegerToBinaryString(code, minCodeLenght)
            compressedContent += converted
        
        return compressedContent
    
    @staticmethod
    def ExtractCodeLenghtAndContent(input, controlBits):
        code_length_bits = input[:controlBits]
        code_length = int(code_length_bits, 2)

        content = input[controlBits:]

        return code_length, content