def create_hex(data):
    # Convert data to bytes
    data_bytes = bytes(data, 'utf-8')
    # Initialize hex result as empty list
    hex_result = []
    # Convert data_bytes to hex of chunk size 16 bytes 
    for i in range(0, len(data_bytes), 16):
        chunk = data_bytes[i:i+16]
        hex_result.append(chunk.hex())
    # Pad the last chunk with 0s if it is less than 32 bytes
    last_chunk = hex_result[-1]
    last_chunk = last_chunk.ljust(32, 'f')
    hex_result[-1] = last_chunk
    # If only one element, XOR it with original data_bytes
    if len(hex_result) == 1:
        xor_result = int(hex_result[0], 16) ^ int(data_bytes.hex(), 16)
    else:
        # Perform XOR operation on each hex term
        xor_result = int(hex_result[0], 16)
        for i in range(1, len(hex_result)):
            xor_result ^= int(hex_result[i], 16)
    # Convert the result back to hex format
    final_hex = hex(xor_result)[2:].zfill(32)
    return final_hex


def round_function(data, key):
    """Custom round function."""
    # Example: Apply a cryptographic hash function to the data with the key
    hash_input = data + key
    hash_output = create_hex(hash_input)
    # print(len(hash_output))
    truncated_hash_output=hash_output
    # print(len(truncated_hash_output))
    return truncated_hash_output

def custom_hash(input_data, rounds=10):
    """Custom 256-bit hash function based on Feistel structure with XOR operations."""
    # Ensure input data length is even
    if len(input_data) % 2 != 0:
        input_data += '\0'  # Pad with null character if needed
    compressed_input=create_hex(input_data)
    # Split input into two equal-sized parts
    # print(len(input_data))
    half_length = len(compressed_input) // 2
    left_part = compressed_input[:half_length]
    right_part = compressed_input[half_length:]
    # print(len(left_part))

    # Convert parts to binary
    left_binary = ''.join(format(ord(char), '08b') for char in left_part)
    right_binary = ''.join(format(ord(char), '08b') for char in right_part)
    # print(len(left_binary))

    for _ in range(rounds):
        # Save original right part
        original_right = right_binary

        # Apply round function to the right part
        round_output = round_function(right_binary, left_binary)
        # print(len(round_output))

        # XOR the result with the left part
        right_binary = '{0:0{1}b}'.format(int(round_output, 16) ^ int(left_binary, 2), len(right_binary))
        # print(len(right_binary))

        # Perform XOR operation between left and right parts
        left_binary = '{0:0{1}b}'.format(int(left_binary, 2) ^ int(original_right, 2), len(left_binary))

    # Combine parts to produce the output hash
    # print(len(left_binary))
    # print(len(right_binary))
    output_hash = left_binary + right_binary

    # Return the hash in hexadecimal format
    return '{0:0{1}x}'.format(int(output_hash, 2), len(output_hash) // 4)
    # return output_hash

input_data = "uzair khan is my name"
# input_data="contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes  1.10.32 and 1.10.33 o"
hash=custom_hash(input_data)
print(hash=="0c50080554570802095456560007010035353134303030353137323039353937")
