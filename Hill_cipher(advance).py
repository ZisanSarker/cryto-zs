# === Helper Functions ===

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

def get_matrix_minor(matrix, i, j):
    return [
        [matrix[row][col] for col in range(len(matrix)) if col != j]
        for row in range(len(matrix)) if row != i
    ]

def matrix_determinant(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0] % 26
    if size == 2:
        return (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]) % 26
    det = 0
    for c in range(size):
        cofactor = ((-1) ** c) * matrix[0][c] * matrix_determinant(get_matrix_minor(matrix, 0, c))
        det = (det + cofactor) % 26
    return det

def matrix_cofactor(matrix):
    size = len(matrix)
    cof = []
    for i in range(size):
        row = []
        for j in range(size):
            minor = get_matrix_minor(matrix, i, j)
            cofactor = ((-1) ** (i + j)) * matrix_determinant(minor)
            row.append(cofactor % 26)
        cof.append(row)
    return cof

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def inverse_matrix(matrix):
    det = matrix_determinant(matrix)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None
    cof = matrix_cofactor(matrix)
    adj = transpose(cof)
    inv = [[(det_inv * adj[i][j]) % 26 for j in range(len(matrix))] for i in range(len(matrix))]
    return inv

def multiply_matrix_vector(matrix, vector):
    result = []
    for row in matrix:
        value = sum(row[i] * vector[i] for i in range(len(vector))) % 26
        result.append(value)
    return result

# === Main Hill Cipher Functions ===

def extract_alpha_blocks(text, size):
    alpha_chars = [(i, c) for i, c in enumerate(text) if c.isalpha()]
    blocks = []
    for i in range(0, len(alpha_chars), size):
        block = alpha_chars[i:i+size]
        if len(block) < size:
            # pad with 'X' (uppercase) as needed
            pad_count = size - len(block)
            for _ in range(pad_count):
                block.append((-1, 'X'))  # virtual padding
        blocks.append(block)
    return blocks

def apply_blocks(text, transformed_blocks):
    result = list(text)
    block_index = 0
    for block in transformed_blocks:
        for (i, _), new_char in block:
            if i == -1:
                continue  # padding
            result[i] = new_char
        block_index += 1
    return ''.join(result)

def hill_encrypt(plaintext, key_matrix):
    size = len(key_matrix)
    blocks = extract_alpha_blocks(plaintext, size)
    encrypted_blocks = []

    for block in blocks:
        nums = [char_to_num(c) for _, c in block]
        upper_flags = [c.isupper() for _, c in block]
        enc = multiply_matrix_vector(key_matrix, nums)
        new_block = [((i, c), num_to_char(n, is_upper=u)) for ((i, c), n, u) in zip(block, enc, upper_flags)]
        encrypted_blocks.append(new_block)

    return apply_blocks(plaintext, encrypted_blocks)

def hill_decrypt(ciphertext, key_matrix):
    size = len(key_matrix)
    inverse_key = inverse_matrix(key_matrix)
    if inverse_key is None:
        raise ValueError("Key matrix is not invertible mod 26.")

    blocks = extract_alpha_blocks(ciphertext, size)
    decrypted_blocks = []

    for block in blocks:
        nums = [char_to_num(c) for _, c in block]
        upper_flags = [c.isupper() for _, c in block]
        dec = multiply_matrix_vector(inverse_key, nums)
        new_block = [((i, c), num_to_char(n, is_upper=u)) for ((i, c), n, u) in zip(block, dec, upper_flags)]
        decrypted_blocks.append(new_block)

    return apply_blocks(ciphertext, decrypted_blocks)

# === Main CLI ===

def main():
    print("=== Hill Cipher (Case & Symbol Preserving, Any n×n Matrix) ===")
    try:
        n = int(input("Enter matrix size (e.g., 2 for 2x2): "))
        if n < 2:
            raise ValueError("Matrix size must be 2 or more.")
    except ValueError as e:
        print("Invalid size:", e)
        return

    try:
        key_input = input(f"🔑 Enter {n * n} numbers for the {n}x{n} matrix (row-wise): ")
        key_values = list(map(int, key_input.strip().split()))
        if len(key_values) != n * n or not all(0 <= k < 26 for k in key_values):
            raise ValueError("Invalid key values.")
    except ValueError as e:
        print("❌ Key matrix error:", e)
        return

    key_matrix = [key_values[i:i+n] for i in range(0, n * n, n)]
    if inverse_matrix(key_matrix) is None:
        print("❌ Key matrix is not invertible mod 26.")
        return

    mode = input("Mode (E = Encrypt, D = Decrypt): ").strip().upper()
    if mode == 'E':
        plaintext = input("Enter plaintext: ")
        ciphertext = hill_encrypt(plaintext, key_matrix)
        print(f"🔒 Ciphertext: {ciphertext}")
    elif mode == 'D':
        ciphertext = input("Enter ciphertext: ")
        try:
            plaintext = hill_decrypt(ciphertext, key_matrix)
            print(f"🔓 Plaintext: {plaintext}")
        except ValueError as e:
            print("❌ Error:", e)
    else:
        print("❌ Invalid mode selected.")

if __name__ == "__main__":
    main()
