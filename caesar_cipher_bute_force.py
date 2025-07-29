def caesar_cipher(text, shift, mode):
    if mode == 'D':
        shift = -shift

    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            result += char  # keep numbers, space, punctuation same
    return result


# --- Brute-force decryption ---
def brute_force_caesar(ciphertext):
    print("\nTrying all possible shifts:\n")
    for shift in range(26):
        possible_plaintext = caesar_cipher(ciphertext, shift, mode='D')
        print(f"Key {shift:2}: {possible_plaintext}")


# --- Main program ---
ciphertext = input("🔐 Enter the ciphertext to brute-force: ")
brute_force_caesar(ciphertext)
