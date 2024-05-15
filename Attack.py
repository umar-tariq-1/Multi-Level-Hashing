import string
import random
import argparse
from Models.Encoder import Encoder


def generate_random_string(length):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def find_second_preimage(hash_function, original_data, hash_value):
    """Find a second pre-image for a given hash value."""
    max_attempts = 10000  # Maximum number of attempts to find a second pre-image
    original_hash = hash_function(original_data)

    for _ in range(max_attempts):
        # Generate a random string of the same length as original_data
        candidate_data = generate_random_string(len(original_data))
        candidate_hex = create_hex(candidate_data)

        # Calculate the hash of the candidate data
        candidate_hash = hash_function(candidate_hex)

        # Check if the candidate data produces the same hash as the original data
        if candidate_hash == hash_value and candidate_data != original_data:
            return candidate_data

    return "Not found within 10,000 iterations."  # Second pre-image not found within the maximum attempts


def attack()->None:
    parser = argparse.ArgumentParser(
        prog="Multi Level Encoder for Hashing",
        description="This program read a file and creates a Merkle Tree ready for Multi-Level Hashing",
        epilog="Created by \033[1mMuhammad Sunaam :)\033[0m"
    )
    parser.add_argument("-f","--file",action='store',help="stores path of the file you want to hash", type=str)
    parser.add_argument("-s","--string",action='store',help="sstring you want to hash", type=str)
    args = parser.parse_args()
    
    if args.file == None and args.string == None:
        print("Usage: -f, --file\tadd path of file to be hashed")
        print("Usage: -s, --string\tstring to be hashed")
        return
    
    if args.file != None:
        encoder = Encoder(args.file, isFile=True)
        print(find_second_preimage(encoder.getHashFunction(),encoder.getOriginalData(),encoder.getFinalHash()))
    else:
        encoder = Encoder(args.string, isFile=False)
    
    
attack()