from BinaryConversor.BinaryConversor import BinaryConversor
from Trie.Trie import Trie

class LZWDecompressor:
    def __init__(self, sigmaSize):
        self.dict = Trie()
        self.sigmaSize = sigmaSize

        # Inicializando o dicionário com as raízes iniciais
        for index in range(sigmaSize):
            bin_key = BinaryConversor.ConvertPrefixToBinaryString(chr(index))
            self.dict[bin_key] = chr(index)

    def Decompress(self, code_length, content):
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

        return ''.join(decompressedList)

    def __getNextCode(self, content, index, code_length):
        code_bits = content[index:index + code_length]
        return code_bits.lstrip('0') or '0'
