class BinaryConversor:
    @staticmethod
    def ConvertBinaryToString(binary):
        if not binary:
            return ""
        
        byte_data = bytes(int(binary[i:i + 8], 2) for i in range(0, len(binary), 8))
        return byte_data.decode('utf-8', errors='ignore')  

    @staticmethod
    def ConvertIntegerToBinaryString(integer, size=0):
        return format(integer, f'0{size}b') if size else bin(integer)[2:]

    @staticmethod
    def ConvertPrefixToBinaryString(prefix):
        return ''.join(BinaryConversor.ConvertIntegerToBinaryString(ord(c)) for c in prefix)
