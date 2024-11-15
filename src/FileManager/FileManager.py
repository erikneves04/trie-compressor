class FileManager:
    @staticmethod
    def ReadFileAsType(filePath, type):
        with open(f"{filePath}", type, encoding="utf-8") as file:
            data = file.read()
        return data
    
    @staticmethod
    def ReadFileAsBinary(filePath):
        data = FileManager.ReadFileAsType(filePath, "rb")
        binary_data = ''.join(format(byte, '08b') for byte in data)
        return binary_data

    @staticmethod
    def ReadFileAsText(filePath):
        return FileManager.ReadFileAsType(filePath, "r")
    
    @staticmethod
    def SaveBinaryFile(filePath, content):
        byte_content = int(content, 2).to_bytes((len(content) + 7) // 8, byteorder='big')
        with open(f"{filePath}", "wb") as file:
            file.write(byte_content)

    @staticmethod
    def SaveTextFile(filePath, content):
        with open(f"{filePath}", "w") as file:
            file.write(content)