alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # 'J' merged with 'I'

def generate_matrix(keyword):
    keyword = keyword.upper().replace('J', 'I')
    matrix = []
    seen = set()
    for char in keyword + alphabet:
        if char in alphabet and char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return -1, -1

def prepare_pairs(text):
    text_letters = []
    text_case_flags = []
    for c in text:
        if c.isalpha():
            text_letters.append(c.upper().replace('J', 'I'))
            text_case_flags.append(c.islower())

    pairs = []
    case_pairs = []
    i = 0
    while i < len(text_letters):
        a = text_letters[i]
        a_case = text_case_flags[i]
        i += 1
        if i < len(text_letters):
            b = text_letters[i]
            if a == b:
                b = 'X'
                b_case = False  # Inserted 'X' is uppercase
            else:
                b_case = text_case_flags[i]
                i += 1
        else:
            b = 'X'
            b_case = False  # Padding 'X' is uppercase
        
        pairs.append((a, b))
        case_pairs.append((a_case, b_case))

    final_case_flags = [case for pair in case_pairs for case in pair]
    return pairs, final_case_flags

def encrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)
    if r1 == r2:
        return matrix[r1][(c1+1)%5], matrix[r2][(c2+1)%5]
    elif c1 == c2:
        return matrix[(r1+1)%5][c1], matrix[(r2+1)%5][c2]
    else:
        return matrix[r1][c2], matrix[r2][c1]

def decrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)
    if r1 == r2:
        return matrix[r1][(c1-1)%5], matrix[r2][(c2-1)%5]
    elif c1 == c2:
        return matrix[(r1-1)%5][c1], matrix[(r2-1)%5][c2]
    else:
        return matrix[r1][c2], matrix[r2][c1]

def playfair_cipher(mode, keyword, message):
    matrix = generate_matrix(keyword)

    if mode == 'E':
        pairs, case_flags = prepare_pairs(message)
        
        result_letters = []
        for a, b in pairs:
            x, y = encrypt_pair(a, b, matrix)
            result_letters.extend([x, y])

        # Rebuild encrypted message
        result_alpha = []
        for i, letter in enumerate(result_letters):
            if case_flags[i]:
                result_alpha.append(letter.lower())
            else:
                result_alpha.append(letter.upper())
        
        result = []
        letter_iter = iter(result_alpha)
        for char in message:
            if char.isalpha():
                result.append(next(letter_iter))
            else:
                result.append(char)
        result.extend(list(letter_iter))
        return "".join(result)

    else:  # Decryption
        letters = [c.upper().replace('J', 'I') for c in message if c.isalpha()]
        case_flags = [c.islower() for c in message if c.isalpha()]

        if len(letters) % 2 != 0:
            print("❌ Invalid ciphertext: odd number of letters.")
            return ""

        pairs = [(letters[i], letters[i+1]) for i in range(0, len(letters), 2)]

        decrypted_letters = []
        for a, b in pairs:
            x, y = decrypt_pair(a, b, matrix)
            decrypted_letters.extend([x, y])
        
        # Heuristically remove inserted 'X's
        final_letters = []
        i = 0
        while i < len(decrypted_letters):
            current_char = decrypted_letters[i]
            next_char = decrypted_letters[i+1] if i + 1 < len(decrypted_letters) else None
            prev_char = final_letters[-1] if final_letters else None

            # Check for X between two identical letters (e.g., LXL from LL)
            if current_char == 'X' and prev_char and prev_char == next_char:
                i += 1 # Skip this 'X'
                continue

            final_letters.append(current_char)
            i += 1
        
        # Remove trailing 'X' if it was likely for padding
        if len(final_letters) % 2 != 0 and final_letters[-1] == 'X':
             final_letters.pop()

        # Rebuild decrypted message
        # Note: This assumes the number of non-alpha chars in ciphertext is what's desired.
        result = []
        letter_iter = iter(final_letters)
        case_iter = iter(case_flags)
        for char in message:
            if char.isalpha():
                try:
                    letter = next(letter_iter)
                    is_lower = next(case_iter)
                    result.append(letter.lower() if is_lower else letter.upper())
                except StopIteration:
                    break 
            else:
                result.append(char)
        return "".join(result)

# ------------------------------
# Main runner
# ------------------------------
if __name__ == "__main__":
    mode = input("🔁 Enter mode (E for Encrypt, D for Decrypt): ").strip().upper()
    keyword = input("🔑 Enter keyword: ").strip()
    message = input("📝 Enter message: ")

    if mode not in ['E', 'D']:
        print("❌ Invalid mode. Use 'E' or 'D'.")
    else:
        result = playfair_cipher(mode, keyword, message)
        print(f"\n🔒 Output ({'Encrypted' if mode == 'E' else 'Decrypted'}): {result}")
