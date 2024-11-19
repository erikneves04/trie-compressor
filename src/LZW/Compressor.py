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

        # Inicializando o dicionário com as raízes iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = index

    def Compress(self, content):
        compressedList = []

        self.prefix = ""
        self.prefixValue = None
        self.biggestCode = self.sigmaSize

        self.currentBits = self.initialBitsSize
        self.maxCode = (1 << self.currentBits) - 1
        
        for char in content:
            prefix_with_char = self.prefix + char

            prefix_key = BinaryConversor.ConvertPrefixToBinaryString(self.prefix)
            prefix_with_char_key = prefix_key + BinaryConversor.ConvertIntegerToBinaryString(ord(char))

            dictValue = self.dict[prefix_with_char_key]
            if dictValue != None:
                self.prefix = prefix_with_char
                self.prefixValue = dictValue
            else:
                if self.dict[prefix_key] == None:
                    self.__insertNewCode(prefix_key)

                value = self.prefixValue if self.prefixValue != None else self.dict[prefix_key]
                compressedList.append(value)

                self.__insertNewCode(prefix_with_char_key)
                self.prefix = char
                self.prefixValue = None
            
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