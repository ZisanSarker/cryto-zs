# Global variables
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = uppercase.lower()
cipher_key_upper = "QWERTYUIOPASDFGHJKLZXCVBNM"  # 26 uppercase letters
cipher_key_lower = cipher_key_upper.lower()       # Build lowercase cipher key from uppercase key

# Validate cipher key
if len(cipher_key_upper) != 26 or sorted(cipher_key_upper) != sorted(uppercase):
    print("Invalid cipher key! Must be 26 unique uppercase letters.")
    exit()

# Encrypt function
def encrypt(plaintext):
    ciphertext = ""
    for char in plaintext:
        if char in uppercase:
            index = uppercase.index(char)
            ciphertext += cipher_key_upper[index]
        elif char in lowercase:
            index = lowercase.index(char)
            ciphertext += cipher_key_lower[index]
        else:
            ciphertext += char
    return ciphertext

# Decrypt function
def decrypt(ciphertext):
    plaintext = ""
    for char in ciphertext:
        if char in cipher_key_upper:
            index = cipher_key_upper.index(char)
            plaintext += uppercase[index]
        elif char in cipher_key_lower:
            index = cipher_key_lower.index(char)
            plaintext += lowercase[index]
        else:
            plaintext += char
    return plaintext

# === Main program ===
mode = input("Enter mode (E for Encrypt, D for Decrypt): ").strip().upper()
if mode == 'E':
    message = input("Enter the message to encrypt: ")
    encrypted = encrypt(message)
    print("Encrypted Message:", encrypted)
elif mode == 'D':
    message = input("Enter the message to decrypt: ")
    decrypted = decrypt(message)
    print("Decrypted Message:", decrypted)
else:
    print("Invalid mode selected! Please choose 'E' or 'D'.")
