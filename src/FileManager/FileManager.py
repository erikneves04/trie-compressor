class FileManager:
    """
    Classe responsável por operações de leitura e escrita de arquivos, incluindo arquivos de texto e binários.
    Suporta operações para arquivos BMP e outros arquivos de texto.
    """

    @staticmethod
    def ReadFile(filePath):
        """
        Lê um arquivo e retorna seu conteúdo como uma string. Caso o arquivo seja do tipo BMP, o conteúdo
        é retornado como uma string binária. Para outros arquivos de texto, o conteúdo é retornado como uma string comum.

        :param filePath: O caminho do arquivo a ser lido.
        :return: Conteúdo do arquivo, sendo uma string binária (para arquivos BMP) ou uma string de texto (para outros arquivos).
        """
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
        """
        Salva o conteúdo fornecido em um arquivo. Se o caminho do arquivo terminar com ".bmp", o conteúdo é
        tratado como um arquivo binário e salvo como BMP. Para outros arquivos, o conteúdo é salvo como texto.

        :param filePath: O caminho onde o arquivo será salvo.
        :param content: O conteúdo a ser salvo no arquivo.
        """
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
        """
        Salva uma string binária em um arquivo como dados binários puros.

        :param filePath: O caminho onde o arquivo binário será salvo.
        :param binaryString: A string binária a ser salva no arquivo.
        """
        byte_array = bytearray()
        for i in range(0, len(binaryString), 8):
            byte = binaryString[i:i + 8]
            byte_array.append(int(byte, 2))

        with open(filePath, "wb") as file:
            file.write(byte_array)

    @staticmethod
    def ReadBinaryFile(filePath):
        """
        Lê um arquivo binário e retorna seu conteúdo como uma string binária.

        :param filePath: O caminho do arquivo binário a ser lido.
        :return: O conteúdo do arquivo binário como uma string binária.
        """
        with open(filePath, "rb") as file:
            byte_data = file.read()

        binaryString = ''.join(bin(byte)[2:].zfill(8) for byte in byte_data)
        return binaryString
