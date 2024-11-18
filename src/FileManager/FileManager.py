class FileManager:
    @staticmethod
    def ReadFile(filePath):
        if filePath.lower().endswith(".bmp"):
            with open(filePath, "rb") as file:
                byte_data = file.read()
            binaryString = ''.join(bin(byte)[2:].zfill(8) for byte in byte_data)
            return binaryString
        else:
            with open(filePath, "r", encoding="utf-8", errors="ignore") as file:
                data = file.read()
            return data

    @staticmethod
    def SaveTextFile(filePath, content):
        if filePath.lower().endswith(".bmp"):
            byte_array = bytearray()
            for i in range(0, len(content), 8):
                byte = content[i:i + 8]
                byte_array.append(int(byte, 2))

            with open(filePath, "wb") as file:
                file.write(byte_array)
        else:
            with open(filePath, "w") as file:
                file.write(content)

    @staticmethod
    def SaveBinaryFile(filePath, binaryString):
        byte_array = bytearray()
        for i in range(0, len(binaryString), 8):
            byte = binaryString[i:i + 8]
            byte_array.append(int(byte, 2))

        with open(filePath, "wb") as file:
            file.write(byte_array)

    @staticmethod
    def ReadBinaryFile(filePath):
        with open(filePath, "rb") as file:
            byte_data = file.read()

        binaryString = ''.join(bin(byte)[2:].zfill(8) for byte in byte_data)
        return binaryString
