class FileManager:
    @staticmethod
    def ReadFile(filePath):
        with open(f"{filePath}", "r", encoding="utf-8") as file:
            data = file.read()
        return data
    
    @staticmethod
    def SaveBinaryFile(filePath, content):
        byte_content = int(content, 2).to_bytes((len(content) + 7) // 8, byteorder='big')
        with open(f"{filePath}", "wb") as file:
            file.write(byte_content)

    @staticmethod
    def SaveTextFile(filePath, content):
        with open(f"{filePath}", "w") as file:
            file.write(content)