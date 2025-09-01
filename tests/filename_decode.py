from argparse import ArgumentParser

LOOKUP_TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+,"

def custom_encode(byte_data: bytes) -> str:
    encoded_str = ""
    ac, bits = 0, 0
    
    for byte in byte_data:
        ac += byte << bits
        bits += 8
        while bits >= 6:
            encoded_str += LOOKUP_TABLE[ac & 0x3f]
            ac >>= 6
            bits -= 6
            
    if bits > 0:
        encoded_str += LOOKUP_TABLE[ac & 0x3f]
    
    return encoded_str

def custom_decode(encoded_str: str) -> bytes:
    reverse_table = {v: k for k, v in enumerate(LOOKUP_TABLE)}
    decoded_bytes = bytearray()
    ac, bits = 0, 0
    
    for char in encoded_str:
        ac += reverse_table[char] << bits
        bits += 6
        while bits >= 8:
            decoded_bytes.append(ac & 0xff)
            ac >>= 8
            bits -= 8
    
    return decoded_bytes

if __name__ == "__main__":
    """
    Example decode and encode functions.
    """
    example_filenames = ["aA+Bb,cC1a2b9FFFSg0z22"]

    for filename in example_filenames:  # As visible when typing 'ls' in a folder with TFFS
        print(f'Filename as listed on a TFFS device: {filename}')
        decoded_bytes = custom_decode(filename)
        print(f'Filename as they should be visible in the binary: {decoded_bytes.hex()}') # These are the bytes that are visible in a hex viewer on the binary itself

        encoded_back = custom_encode(decoded_bytes)
        print(f'Filename as listed on a TFFS device: {encoded_back}')  # Should match the original `encoded_str` -> Verify??