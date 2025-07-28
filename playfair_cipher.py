alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

def generate_matrix(keyword):
    keyword = keyword.upper().replace('J', 'I')
    matrix = []
    used = set()

    for char in keyword + alphabet:
        if char not in used and char in alphabet:
            used.add(char)
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None

def prepare_text(text, mode):
    cleaned = []
    positions = []

    for i, c in enumerate(text):
        if c.isalpha():
            c = c.upper().replace('J', 'I')
            cleaned.append(c)
            positions.append(i)

    pairs = []
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        if i + 1 < len(cleaned):
            b = cleaned[i + 1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
        else:
            b = 'X'
            i += 1
        pairs.append((a, b))

    return pairs, positions

def encrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def playfair_cipher(mode, key, message):
    matrix = generate_matrix(key)
    pairs, positions = prepare_text(message, mode)
    result = ""

    for a, b in pairs:
        if mode.upper() == 'E':
            result += encrypt_pair(a, b, matrix)
        elif mode.upper() == 'D':
            result += decrypt_pair(a, b, matrix)

    # Re-insert non-alphabetic characters
    final_text = list(message)
    idx = 0
    for i in range(len(final_text)):
        if final_text[i].isalpha():
            final_text[i] = result[idx]
            idx += 1

    return ''.join(final_text)

# 🔽 Input & Output
if __name__ == "__main__":
    mode = input("🔁 Enter mode (E for Encrypt, D for Decrypt): ").strip().upper()
    key = input("🔑 Enter keyword: ").strip()
    message = input("📝 Enter message: ")

    output = playfair_cipher(mode, key, message)
    print(f"\n🔒 Output ({'Encrypted' if mode == 'E' else 'Decrypted'}): {output}")
