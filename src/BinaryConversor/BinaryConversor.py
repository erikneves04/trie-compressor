class BinaryConversor:
    """
    Classe utilitária para conversões binárias, incluindo conversão de binário 
    para string, inteiro para binário e prefixo para string binária.
    """

    @staticmethod
    def ConvertBinaryToString(binary):
        """
        Converte uma string binária em uma string ascii.

        :param binary: Uma string composta por dígitos binários.
        :return: String decodificada em UTF-8. Partes não decodificáveis são ignoradas.
        """
        if not binary:
            return ""
        
        byte_data = bytes(int(binary[i:i + 8], 2) for i in range(0, len(binary), 8))
        return byte_data.decode('utf-8', errors='ignore')

    @staticmethod
    def ConvertIntegerToBinaryString(integer, size=0):
        """
        Converte um número inteiro para sua representação como string binária.

        :param integer: O número inteiro a ser convertido.
        :param size: Tamanho mínimo da string binária resultante (com preenchimento 
                     de zeros à esquerda). Padrão é 0 (sem preenchimento).
        :return: Representação binária do número inteiro.
        """
        return format(integer, f'0{size}b') if size else bin(integer)[2:]

    @staticmethod
    def ConvertPrefixToBinaryString(prefix):
        """
        Converte um prefixo de string para sua representação em string binária.

        :param prefix: O prefixo de string a ser convertido.
        :return: Representação binária do prefixo.
        """
        return ''.join(BinaryConversor.ConvertIntegerToBinaryString(ord(c)) for c in prefix)
