BLOCK_SIZE = 8

def str_to_bits(s):
    return ''.join(f'{ord(c):08b}' for c in s)

def bits_to_str(b):
    return ''.join(chr(int(b[i:i+8],2)) for i in range(0, len(b), 8))

def xor_bits(a, b):
    return ''.join(str(int(a[i]^int[b[i%len(b)]])) for i in range(len(a)))

