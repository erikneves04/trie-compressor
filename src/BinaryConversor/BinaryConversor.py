class BinaryConversor:
    @staticmethod
    def ConvertBinaryToString(binary):
        if not binary:
            return ""
        
        byte_array = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        byte_data = bytes(int(byte, 2) for byte in byte_array)
        return byte_data.decode('utf-8')
    
    @staticmethod
    def ConvertIntegerToBinaryString(integer, size = 0):
        binary_str = bin(integer)[2:]
        binary_str = binary_str.zfill(size)
        
        return binary_str
    
    @staticmethod
    def ConvertPrefixToBinaryString(prefix):
        binary_parts = [BinaryConversor.ConvertIntegerToBinaryString(ord(c)) for c in prefix]
        return ''.join(binary_parts)