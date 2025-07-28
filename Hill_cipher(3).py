# --- Utility Functions ---

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def clean_text(text):
    text = ''.join(filter(str.isalpha, text)).upper()
    while len(text) % 3 != 0:
        text += 'X'
    return text

def mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def multiply_matrix_vector(matrix, vector):
    result = []
    for row in matrix:
        val = sum(row[i] * vector[i] for i in range(3)) % 26
        result.append(val)
    return result

def matrix_determinant_3x3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)) % 26
    return det

def matrix_cofactor_3x3(m):
    cof = [[0]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            minor = [
                [m[i][j] for j in range(3) if j != c]
                for i in range(3) if i != r
            ]
            val = minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0]
            cof[r][c] = ((-1)**(r+c)) * val % 26
    return cof

def transpose(matrix):
    return [[matrix[j][i] for j in range(3)] for i in range(3)]

def inverse_matrix_3x3(matrix):
    det = matrix_determinant_3x3(matrix)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None
    cof = matrix_cofactor_3x3(matrix)
    adj = transpose(cof)
    inv = [[(det_inv * adj[r][c]) % 26 for c in range(3)] for r in range(3)]
    return inv

# --- Cipher Functions ---

def hill_encrypt(plaintext, key_matrix):
    plaintext = clean_text(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), 3):
        block = [char_to_num(plaintext[i+j]) for j in range(3)]
        enc = multiply_matrix_vector(key_matrix, block)
        ciphertext += ''.join(num_to_char(n) for n in enc)
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    inv_matrix = inverse_matrix_3x3(key_matrix)
    if inv_matrix is None:
        raise ValueError("Key matrix is not invertible mod 26.")
    plaintext = ""
    for i in range(0, len(ciphertext), 3):
        block = [char_to_num(ciphertext[i+j]) for j in range(3)]
        dec = multiply_matrix_vector(inv_matrix, block)
        plaintext += ''.join(num_to_char(n) for n in dec)
    return plaintext

# --- Main ---

def main():
    print("== Hill Cipher (3x3 Matrix Input in One Line) ==")

    try:
        key_input = input("🔑 Enter 9 numbers for the key matrix (space-separated): ")
        key_list = list(map(int, key_input.strip().split()))
        if len(key_list) != 9 or not all(0 <= x <= 25 for x in key_list):
            raise ValueError("You must enter exactly 9 integers between 0 and 25.")
        key_matrix = [key_list[i:i+3] for i in range(0, 9, 3)]
    except ValueError as e:
        print("❌ Invalid input:", e)
        return

    if inverse_matrix_3x3(key_matrix) is None:
        print("❌ Error: Key matrix is not invertible mod 26.")
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
