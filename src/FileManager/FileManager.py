class FileManager:
    @staticmethod
    def ReadFileAsBinary(filePath):
        with open(f"{filePath}", "rb") as file:
            byte_data = file.read()

        binary_data = ''.join(format(byte, '08b') for byte in byte_data)
        return binary_data

    @staticmethod
    def ConvertBinaryToString(binary):
        if not binary:
            return ""
        
        byte_array = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        byte_data = bytes(int(byte, 2) for byte in byte_array)
        return byte_data.decode('utf-8')

    @staticmethod
    def SaveFile(filePath, content):
        with open(f"{filePath}", "w") as file:
            file.write(content)