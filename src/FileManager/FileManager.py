class FileManager:
    @staticmethod
    def ReadFile(filePath):
        with open(f"{filePath}", "r", encoding="utf-8", errors="ignore") as file:
            data = file.read()
        return data

    @staticmethod
    def SaveTextFile(filePath, content):
        with open(f"{filePath}", "w") as file:
            file.write(content)

    @staticmethod
    def SaveBinaryFile(filePath, binaryString):
        # Converter a string binária para uma sequência de bytes
        byte_array = bytearray()
        for i in range(0, len(binaryString), 8):
            # Converter cada grupo de 8 bits para um byte
            byte = binaryString[i:i + 8]
            byte_array.append(int(byte, 2))

        # Salvar o arquivo como binário
        with open(filePath, "wb") as file:
            file.write(byte_array)

    @staticmethod
    def ReadBinaryFile(filePath):
        # Ler o arquivo binário
        with open(filePath, "rb") as file:
            byte_data = file.read()

        # Converter de volta para string binária, respeitando o conteúdo original
        binaryString = ''.join(bin(byte)[2:].zfill(8) for byte in byte_data)
        return binaryString
