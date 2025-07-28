def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n, is_upper=True):
    base = ord('A') if is_upper else ord('a')
    return chr((n % 26) + base)

def mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def inverse_matrix_2x2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    det = (a * d - b * c) % 26
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None
    return [
        [( d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, ( a * det_inv) % 26]
    ]

def matrix_multiply_2x2_vector(matrix, vector):
    return [
        (matrix[0][0]*vector[0] + matrix[0][1]*vector[1]) % 26,
        (matrix[1][0]*vector[0] + matrix[1][1]*vector[1]) % 26
    ]

def hill_encrypt(text, key_matrix):
    result = []
    i = 0
    while i < len(text):
        if text[i].isalpha():
            c1 = text[i]
            j = i + 1
            while j < len(text) and not text[j].isalpha():
                j += 1
            c2 = text[j] if j < len(text) else 'X'
            v1, v2 = char_to_num(c1), char_to_num(c2)
            enc = matrix_multiply_2x2_vector(key_matrix, [v1, v2])
            result.append(num_to_char(enc[0], c1.isupper()))
            for k in range(i+1, j):
                result.append(text[k])
            result.append(num_to_char(enc[1], c2.isupper() if j < len(text) else True))
            i = j + 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

def hill_decrypt(text, key_matrix):
    inv_key = inverse_matrix_2x2(key_matrix)
    if inv_key is None:
        raise ValueError("Key matrix is not invertible modulo 26.")
    result = []
    i = 0
    while i < len(text):
        if text[i].isalpha():
            c1 = text[i]
            j = i + 1
            while j < len(text) and not text[j].isalpha():
                j += 1
            c2 = text[j] if j < len(text) else 'X'
            v1, v2 = char_to_num(c1), char_to_num(c2)
            dec = matrix_multiply_2x2_vector(inv_key, [v1, v2])
            result.append(num_to_char(dec[0], c1.isupper()))
            for k in range(i+1, j):
                result.append(text[k])
            result.append(num_to_char(dec[1], c2.isupper() if j < len(text) else True))
            i = j + 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

print("== Hill Cipher (2x2) with case & symbols preserved ==")
key_input = input("Enter 4 numbers (0-25) for key matrix (row-wise): ")
vals = list(map(int, key_input.strip().split()))
if len(vals) != 4 or any(not (0 <= v <= 25) for v in vals):
    print("Invalid key matrix input. Must be 4 numbers between 0 and 25.")
    exit()

key = [vals[:2], vals[2:]]

if inverse_matrix_2x2(key) is None:
    print("Key matrix is not invertible mod 26.")
    exit()

mode = input("Mode (E=Encrypt, D=Decrypt): ").strip().upper()
if mode == 'E':
    plaintext = input("Enter plaintext: ")
    print("Ciphertext:", hill_encrypt(plaintext, key))
elif mode == 'D':
    ciphertext = input("Enter ciphertext: ")
    try:
        print("Plaintext:", hill_decrypt(ciphertext, key))
    except ValueError as e:
        print("Error:", e)
else:
    print("Invalid mode. Use E or D.")
