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

def ofb_encrypt_decrypt(bits_input, key, iv):
    print("\n🔁 OFB Encryption/Decryption")
    key_bits = str_to_bits(key)
    iv_bits = str_to_bits(iv)[:BLOCK_SIZE]
    bits = pad_bits(bits_input)
    blocks = split_blocks(bits)

    print(f"Input bits:  {bits}")
    print(f"Key bits:    {key_bits}")
    print(f"IV bits:     {iv_bits}")

    output_blocks = []
    prev_output = iv_bits

    for i, block in enumerate(blocks):
        stream_output = xor_bits(prev_output, key_bits)  # simulate E(prev_output)
        result_block = xor_bits(block, stream_output)
        print(f"\nBlock {i+1}:")
        print(f"  OFB stream:   {prev_output} XOR {key_bits[:BLOCK_SIZE]} = {stream_output}")
        print(f"  Input XOR:    {block} XOR {stream_output} = {result_block}")
        output_blocks.append(result_block)
        prev_output = stream_output

    return ''.join(output_blocks)

# --- Test OFB ---
plaintext = "Hi"
key = "K"
iv = "Z"

# Step 1: Convert plaintext to bits
plaintext_bits = str_to_bits(plaintext)
original_bit_len = len(plaintext_bits)

# Step 2: Encrypt
cipher_bits = ofb_encrypt_decrypt(plaintext_bits, key, iv)
print(f"\n🧾 Ciphertext bits: {cipher_bits}")

# Step 3: Decrypt using same function (because OFB is symmetric)
recovered_bits = ofb_encrypt_decrypt(cipher_bits, key, iv)

# Step 4: Trim to original bit length
recovered_bits = recovered_bits[:original_bit_len]

# Step 5: Convert bits to string
recovered_text = bits_to_str(recovered_bits)
print(f"\n📝 Decrypted text: '{recovered_text}'")
