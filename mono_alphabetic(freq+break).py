from collections import Counter

# ================================
# 🌍 Global Variables
# ================================
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = "abcdefghijklmnopqrstuvwxyz"
cipher_key_upper = "QWERTYUIOPASDFGHJKLZXCVBNM"  # 26 uppercase letters

# Validate the cipher key
if len(cipher_key_upper) != 26 or sorted(cipher_key_upper) != sorted(uppercase):
    print("❌ Invalid cipher key! It must contain all 26 unique uppercase letters.")
    exit()

cipher_key_lower = cipher_key_upper.lower()


# ================================
# 🔐 Encrypt Function
# ================================
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


# ================================
# 🔓 Decrypt Function
# ================================
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


# ================================
# 📊 Frequency Analysis
# ================================
def frequency_analysis(text):
    print("\n📊 Relative Frequency Analysis:")
    text = ''.join([c.upper() for c in text if c.isalpha()])
    total = len(text)
    count = Counter(text)
    for letter, freq in count.most_common():
        percentage = (freq / total) * 100
        print(f"{letter}: {freq} ({percentage:.2f}%)")


# ================================
# 🧠 Break Cipher (Guess)
# ================================
def break_cipher(ciphertext):
    print("\n🧠 Breaking Cipher using English Letter Frequency...")
    english_freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

    # Get most frequent letters in ciphertext
    text_only = [c.upper() for c in ciphertext if c.isalpha()]
    cipher_count = Counter(text_only)
    sorted_cipher_letters = [item[0] for item in cipher_count.most_common()]

    # Build guess mapping
    guess_map = {}
    for i in range(min(len(sorted_cipher_letters), len(english_freq_order))):
        cipher_letter = sorted_cipher_letters[i]
        guess_letter = english_freq_order[i]
        guess_map[cipher_letter] = guess_letter

    # Apply guess map
    guessed_plaintext = ""
    for char in ciphertext:
        if char.upper() in guess_map:
            guessed = guess_map[char.upper()]
            guessed_plaintext += guessed.lower() if char.islower() else guessed
        else:
            guessed_plaintext += char

    print("🔍 Guessed Decryption (Approximate):")
    return guessed_plaintext


# ================================
# 🧪 Main Program
# ================================
plaintext = input("📝 Enter the message to encrypt: ")

encrypted = encrypt(plaintext)
print("\n🔐 Encrypted Message:", encrypted)

decrypted = decrypt(encrypted)
print("🔓 Decrypted Message:", decrypted)

frequency_analysis(encrypted)

guessed = break_cipher(encrypted)
print(guessed)
