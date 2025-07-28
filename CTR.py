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

def int_to_bin(counter, length):
    return f'{counter:0{length}b}'[-length:]

def ctr_process(input_text, key, nonce):
    print("\n🔁 CTR Encryption/Decryption")
    bits = str_to_bits(input_text)
    key_bits = str_to_bits(key)
    nonce_bits = str_to_bits(nonce)[:BLOCK_SIZE]
    bits = pad_bits(bits)
    blocks = split_blocks(bits)

    print(f"Input bits:  {bits}")
    print(f"Key bits:    {key_bits}")
    print(f"Nonce bits:  {nonce_bits}")

    output_blocks = []

    for i, block in enumerate(blocks):
        counter_bits = int_to_bin(i, BLOCK_SIZE)
        ctr_input = xor_bits(nonce_bits, counter_bits)  # simulate nonce + counter (XOR for demo)
        encrypted_ctr = xor_bits(ctr_input, key_bits)   # simulate E(nonce+counter)
        result_block = xor_bits(block, encrypted_ctr)
        print(f"\nBlock {i+1}:")
        print(f"  Counter bits: {counter_bits}")
        print(f"  Nonce XOR Counter: {nonce_bits} XOR {counter_bits} = {ctr_input}")
        print(f"  Encrypted CTR:     {ctr_input} XOR {key_bits[:BLOCK_SIZE]} = {encrypted_ctr}")
        print(f"  Input XOR:         {block} XOR {encrypted_ctr} = {result_block}")
        output_blocks.append(result_block)

    return ''.join(output_blocks)

# --- Test CTR ---
plaintext = "Hi"
key = "K"
nonce = "N"  # acts as fixed IV or nonce

cipher = ctr_process(plaintext, key, nonce)
print(f"\n🧾 Ciphertext bits: {cipher}")

# Decrypt: convert cipher bits to string before decrypting
cipher_text_as_str = bits_to_str(cipher)

recovered_bits = ctr_process(cipher_text_as_str, key, nonce)
recovered_text = bits_to_str(recovered_bits).rstrip('\x00')

print(f"\n📝 Decrypted text: '{recovered_text}'")