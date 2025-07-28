# Block size in bits
BLOCK_SIZE = 8

def str_to_bits(s):
    return ''.join(f'{ord(c):08b}' for c in s)

def bits_to_str(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def xor_bits(block, key):
    return ''.join(str(int(block[i]) ^ int(key[i % len(key)])) for i in range(len(block)))

def pad_bits(bits):
    pad_len = BLOCK_SIZE - (len(bits) % BLOCK_SIZE)
    return bits + '0' * pad_len  # Padding with zeros for simplicity

def split_blocks(bits):
    return [bits[i:i+BLOCK_SIZE] for i in range(0, len(bits), BLOCK_SIZE)]

# Encrypt using ECB
def ecb_encrypt(plaintext, key):
    print("\n🔒 ECB Encryption")
    bits = str_to_bits(plaintext)
    key_bits = str_to_bits(key)
    bits = pad_bits(bits)
    blocks = split_blocks(bits)
    
    print(f"Plaintext bits: {bits}")
    print(f"Key bits:       {key_bits}")

    ciphertext_blocks = []
    for i, block in enumerate(blocks):
        encrypted = xor_bits(block, key_bits)
        print(f"Block {i+1}: {block} XOR {key_bits[:len(block)]} = {encrypted}")
        ciphertext_blocks.append(encrypted)

    return ''.join(ciphertext_blocks)

# Decrypt using ECB
def ecb_decrypt(cipher_bits, key):
    print("\n🔓 ECB Decryption")
    key_bits = str_to_bits(key)
    blocks = split_blocks(cipher_bits)
    
    plaintext_blocks = []
    for i, block in enumerate(blocks):
        decrypted = xor_bits(block, key_bits)
        print(f"Block {i+1}: {block} XOR {key_bits[:len(block)]} = {decrypted}")
        plaintext_blocks.append(decrypted)

    return bits_to_str(''.join(plaintext_blocks)).rstrip('\x00')  # Remove null padding
# --- Test ECB ---
plaintext = "Hi"
key = "K"  # 1-char = 8 bits

cipher = ecb_encrypt(plaintext, key)
print(f"\n🧾 Ciphertext bits: {cipher}")

recovered = ecb_decrypt(cipher, key)
print(f"\n📝 Decrypted text: '{recovered}'")
