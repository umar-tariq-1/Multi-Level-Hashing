import os

class HashFunc:
    def __init__(self):
        pass
    
    @staticmethod
    def create_hex(input_data: str) -> str:
        """
        Creates a simple non-linear transformation to produce a hexadecimal representation of the input data.
        
        Parameters:
            input_data (str): The input data to transform.
            
        Returns:
            str: The hexadecimal representation of the transformed data.
        """
        data_bytes = bytes(input_data, 'utf-8')
        hex_result = []
        for i in range(0, len(data_bytes), 16):
            chunk = data_bytes[i:i+16]
            hex_chunk = ''.join(f'{byte:02x}' for byte in chunk)
            hex_result.append(hex_chunk)
        
        if hex_result:
            last_chunk = hex_result[-1].ljust(32, 'c')
            hex_result[-1] = last_chunk
        
        if len(hex_result) == 1:
            xor_result = int(hex_result[0], 16) ^ int(data_bytes.hex(), 16)
        else:
            xor_result = int(hex_result[0], 16)
            for chunk in hex_result[1:]:
                xor_result ^= int(chunk, 16)
        
        final_hex = f'{xor_result:032x}'
        return final_hex
    
    @classmethod
    def round_function(cls, data: str, key: str) -> str:
        """
        Performs a simple shuffle and append round function.
        
        Parameters:
            data (str): The data to be transformed.
            key (str): The key used for the transformation.
            
        Returns:
            str: The transformed data.
        """
        hash_input = data + key
        hash_output = HashFunc.create_hex(hash_input)
        return hash_output[:32]
    
    @staticmethod    
    def custom_hash(input_data: str, rounds=10, salt_length=16) -> str:
        """
        Generates a custom hash value for the input data.
        
        Parameters:
            input_data (str): The data to be hashed.
            rounds (int): The number of hashing rounds.
            salt_length (int): The length of the salt in bytes.
            
        Returns:
            str: The hashed value of the input data.
        """
        salt = "581756ef16edad700121d3e0e7c4dac3"
        
        compressed_input = HashFunc.create_hex(input_data + salt)
        half_length = len(compressed_input) // 2
        left_part = compressed_input[:half_length]
        right_part = compressed_input[half_length:]
        
        left_binary = ''.join(format(int(char, 16), '04b') for char in left_part)
        right_binary = ''.join(format(int(char, 16), '04b') for char in right_part)
        
        for _ in range(rounds):
            original_right = right_binary

            round_output = HashFunc.round_function(right_binary, left_binary)

            right_binary = '{0:0{1}b}'.format(int(round_output, 16) ^ int(left_binary, 2), len(right_binary))
            
            left_binary = '{0:0{1}b}'.format(int(left_binary, 2) ^ int(original_right, 2), len(left_binary))

        output_hash = left_binary + right_binary

        return '{0:0{1}x}'.format(int(output_hash, 2), len(output_hash) // 4)
