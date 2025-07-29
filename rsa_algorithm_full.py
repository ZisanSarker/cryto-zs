# RSA Encryption and Decryption using Extended Euclidean Algorithm

# === Extended Euclidean Algorithm ===
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# === Modular Inverse using EEA ===
def mod_inverse(e, phi):
    gcd, x, _ = egcd(e, phi)
    if gcd != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi

# === RSA Encryption: C = M^e mod n ===
def encrypt(M, e, n):
    return pow(M, e, n)

# === RSA Decryption: M = C^d mod n ===
def decrypt(C, d, n):
    return pow(C, d, n)

# === Convert text (A-Z and space) to number (01 = A, ..., 26 = Z, 27 = space) ===
def letters_to_number(text):
    mapping = {chr(64 + i): f"{i:02d}" for i in range(1, 27)}
    mapping[' '] = "27"
    number = ""
    for char in text.upper():
        if char in mapping:
            number += mapping[char]
    return int(number)

# === Convert number to text ===
def number_to_letters(number):
    mapping = {i: chr(64 + i) for i in range(1, 27)}
    mapping[27] = ' '
    s = str(number)
    if len(s) % 2 != 0:
        s = '0' + s
    letters = ""
    for i in range(0, len(s), 2):
        num = int(s[i:i+2])
        letters += mapping.get(num, '')
    return letters.strip()

# === INPUT ===
print("=== RSA Setup ===")
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))
e = int(input("Enter public exponent e (such that gcd(e, (p-1)*(q-1)) = 1): "))

# === Key Generation ===
n = p * q
phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

# === Show Keys ===
print(f"\nPublic Key  (e, n): ({e}, {n})")
print(f"Private Key (d, n): ({d}, {n})")

# === Plaintext Input and Encryption ===
plaintext = input("\nEnter plaintext message (only A-Z and space): ").upper()
M = letters_to_number(plaintext)
C = encrypt(M, e, n)

# === Ciphertext Output ===
print(f"\nEncrypted numeric message: {C}")

# === Decryption ===
M_decrypted = decrypt(C, d, n)
decrypted_text = number_to_letters(M_decrypted)

# === Final Output ===
print(f"Decrypted numeric message: {M_decrypted}")
print(f"Decrypted plaintext message: {decrypted_text}")
