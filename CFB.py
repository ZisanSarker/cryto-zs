BLOCK_SIZE = 8  # bits per block

def str_to_bits(s):
    return ''.join(f'{ord(c):08b}' for c in s)

def bits_to_str(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def xor_bits(a, b):
    return ''.join(str(int(a[i]) ^ int(b[i % len(b)])) for i in range(len(a)))

def pad_bits(bits):
    pad_len = BLOCK_SIZE - (len(bits) % BLOCK_SIZE)
    return bits + '0' * pad_len

def split_blocks(bits):
    return [bits[i:i+BLOCK_SIZE] for i in range(0, len(bits), BLOCK_SIZE)]

def cfb_encrypt(plaintext, key, iv):
    print("\n🔒 CFB Encryption")
    bits = str_to_bits(plaintext)
    key_bits = str_to_bits(key)
    iv_bits = str_to_bits(iv)[:BLOCK_SIZE]
    bits = pad_bits(bits)
    blocks = split_blocks(bits)

    print(f"Plaintext bits: {bits}")
    print(f"Key bits:       {key_bits}")
    print(f"IV bits:        {iv_bits}")

    ciphertext_blocks = []
    prev_cipher = iv_bits

    for i, block in enumerate(blocks):
        encrypted = xor_bits(prev_cipher, key_bits)  # simulate E(prev_cipher)
        cipher_block = xor_bits(block, encrypted)
        print(f"\nBlock {i+1}:")
        print(f"  Input:         {block}")
        print(f"  E(prev):       {prev_cipher} XOR {key_bits[:BLOCK_SIZE]} = {encrypted}")
        print(f"  Cipher block:  {block} XOR {encrypted} = {cipher_block}")
        ciphertext_blocks.append(cipher_block)
        prev_cipher = cipher_block

    return ''.join(ciphertext_blocks)

def cfb_decrypt(ciphertext_bits, key, iv):
    print("\n🔓 CFB Decryption")
    key_bits = str_to_bits(key)
    iv_bits = str_to_bits(iv)[:BLOCK_SIZE]
    blocks = split_blocks(ciphertext_bits)

    plaintext_blocks = []
    prev_cipher = iv_bits

    for i, block in enumerate(blocks):
        encrypted = xor_bits(prev_cipher, key_bits)  # simulate E(prev_cipher)
        plain_block = xor_bits(block, encrypted)
        print(f"\nBlock {i+1}:")
        print(f"  Cipher block:  {block}")
        print(f"  E(prev):       {prev_cipher} XOR {key_bits[:BLOCK_SIZE]} = {encrypted}")
        print(f"  Plain block:   {block} XOR {encrypted} = {plain_block}")
        plaintext_blocks.append(plain_block)
        prev_cipher = block

    return bits_to_str(''.join(plaintext_blocks)).rstrip('\x00')

# --- Test CFB ---
plaintext = "Hi"
key = "K"
iv = "Z"

cipher = cfb_encrypt(plaintext, key, iv)
print(f"\n🧾 Ciphertext bits: {cipher}")

recovered = cfb_decrypt(cipher, key, iv)
print(f"\n📝 Decrypted text: '{recovered}'")
