class HashFunc:
    def __init__(self)->None:
        pass
    
    @classmethod
    def create_hex(cls, input_data:str)->str:
        
        """
        Creates Hexadecimal Representation of Data
        Returns 
            str: Hexadecimal value of data
        """
        
        data_bytes = bytes(input_data, 'utf-8')
        hex_result = []
        for i in range(0, len(data_bytes), 16):
            chunk = data_bytes[i:i+16]
            hex_result.append(chunk.hex())
        last_chunk = hex_result[-1]
        last_chunk = last_chunk.ljust(32, 'f')
        hex_result[-1] = last_chunk
        if len(hex_result) == 1:
            xor_result = int(hex_result[0], 16) ^ int(data_bytes.hex(), 16)
        else:
            xor_result = int(hex_result[0], 16)
            for i in range(1, len(hex_result)):
                xor_result ^= int(hex_result[i], 16)
        final_hex = hex(xor_result)[2:].zfill(32)
        return final_hex
    
    @classmethod
    def round_function(cls,data:str, key:str)->str:
        
        """
        Shuffles and Appends
        
        Parameters:
            data(str): Input Data
            key(str): Input Key
            
        Returns:
            str: The shuffled round output
        """
        
        hash_input = data + key
        hash_output = HashFunc.create_hex(hash_input)
        truncated_hash_output=hash_output
        return truncated_hash_output
    
    @staticmethod    
    def custom_hash(input_data:str, rounds=10)->str:
        
        """
        Returns hashed value of input data
        
        Parameters:
            input_data(str): Data to be hashed
            rounds(int): Number of rounds
        
        Returns
            str: The hashed value of the input_data 
        """
        
        if len(input_data) % 2 != 0:
            input_data += '\0'  # Pad with null character if needed
        compressed_input=HashFunc.create_hex(input_data)
        half_length = len(compressed_input) // 2
        left_part = compressed_input[:half_length]
        right_part = compressed_input[half_length:]

        left_binary = ''.join(format(ord(char), '08b') for char in left_part)
        right_binary = ''.join(format(ord(char), '08b') for char in right_part)

        for _ in range(rounds):
            original_right = right_binary

            round_output = HashFunc.round_function(right_binary, left_binary)

            right_binary = '{0:0{1}b}'.format(int(round_output, 16) ^ int(left_binary, 2), len(right_binary))

            left_binary = '{0:0{1}b}'.format(int(left_binary, 2) ^ int(original_right, 2), len(left_binary))

        output_hash = left_binary + right_binary

        return '{0:0{1}x}'.format(int(output_hash, 2), len(output_hash) // 4)