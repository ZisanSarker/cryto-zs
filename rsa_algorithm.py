# Extended Euclidean Algorithm to find gcd and modular inverse
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# Finds modular inverse of e mod phi
def mod_inverse(e, phi):
    gcd, x, _ = egcd(e, phi)
    if gcd != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi

# RSA decryption: M = C^d mod n
def decrypt(C, d, n):
    return pow(C, d, n)

# Converts 4-digit number to 2 letters (01 = A, ..., 26 = Z, 27 = space)
def number_to_letters(number):
    mapping = {i: chr(64 + i) for i in range(1, 27)}
    mapping[27] = ' '
    s = str(number)
    
    if len(s) % 2 != 0:
        s = '0' + s  # Add padding to make even number of digits

    letters = ""
    for i in range(0, len(s), 2):
        num = int(s[i:i+2])
        letters += mapping.get(num, '')
    return letters.strip()


# === Input ===
p = int(input("Enter prime p: "))
q = int(input("Enter prime q: "))
e = int(input("Enter public exponent e: "))
C = int(input("Enter ciphertext C: "))

# === Key Generation ===
n = p * q

phi = (p - 1) * (q - 1) # Compute Euler's Totient function phi(n)
d = mod_inverse(e, phi)

# === Decryption ===
M = decrypt(C, d, n)
plaintext = number_to_letters(M)

# === Output ===
print(f"\nPublic Key  PU = {{e={e}, n={n}}}")
print(f"Private Key PR = {{d={d}, n={n}}}")
print(f"Decrypted number M = {M}")
print(f"Decrypted plaintext: {plaintext}")
print(f"Ciphertext C = {C}")
