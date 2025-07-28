# === Helper Functions ===

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def clean_text(text, block_size):
    text = ''.join(filter(str.isalpha, text)).upper()
    while len(text) % block_size != 0:
        text += 'X'
    return text

def mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_matrix_minor(matrix, i, j):
    # Remove row i and column j from matrix
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

# === Hill Cipher Logic ===

def hill_encrypt(plaintext, key_matrix):
    size = len(key_matrix)
    plaintext = clean_text(plaintext, size)
    ciphertext = ''
    for i in range(0, len(plaintext), size):
        block = [char_to_num(c) for c in plaintext[i:i+size]]
        enc = multiply_matrix_vector(key_matrix, block)
        ciphertext += ''.join(num_to_char(n) for n in enc)
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    size = len(key_matrix)
    inverse_key = inverse_matrix(key_matrix)
    if inverse_key is None:
        raise ValueError("Key matrix is not invertible modulo 26.")
    plaintext = ''
    for i in range(0, len(ciphertext), size):
        block = [char_to_num(c) for c in ciphertext[i:i+size]]
        dec = multiply_matrix_vector(inverse_key, block)
        plaintext += ''.join(num_to_char(n) for n in dec)
    return plaintext

# === Main Driver ===

def main():
    print("=== General Hill Cipher (n x n) ===")

    try:
        n = int(input("Enter size of key matrix (e.g., 2 for 2x2, 3 for 3x3): "))
        if n < 2:
            raise ValueError("Matrix size must be 2 or more.")
    except ValueError as e:
        print("Invalid input:", e)
        return

    try:
        key_input = input(f"🔑 Enter {n * n} numbers for the {n}x{n} key matrix (row-wise, space-separated): ")
        key_values = list(map(int, key_input.strip().split()))
        if len(key_values) != n * n or not all(0 <= k <= 25 for k in key_values):
            raise ValueError("Invalid number of elements or values out of range.")
    except ValueError as e:
        print("❌ Invalid key matrix input:", e)
        return

    key_matrix = [key_values[i:i+n] for i in range(0, n * n, n)]

    if inverse_matrix(key_matrix) is None:
        print("❌ Key matrix is not invertible mod 26.")
        return

    mode = input("📝 Enter mode (E = Encrypt, D = Decrypt): ").strip().upper()
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
        print("❌ Invalid mode. Use 'E' or 'D'.")

if __name__ == "__main__":
    main()
