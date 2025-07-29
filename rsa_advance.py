# === Extended Euclidean Algorithm ===
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# === Modular Inverse ===
def mod_inverse(e, phi):
    gcd, x, _ = egcd(e, phi)
    if gcd != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi

# === Prime Check ===
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# === RSA Encryption/Decryption ===
def encrypt(M, e, n):
    return pow(M, e, n)

def decrypt(C, d, n):
    return pow(C, d, n)

# === Convert text to number using 3-digit ASCII codes ===
def text_to_number(text):
    return int(''.join(f"{ord(c):03d}" for c in text))

# === Convert number back to text ===
def number_to_text(number):
    s = str(number)
    # Pad to make length a multiple of 3
    if len(s) % 3 != 0:
        s = '0' * (3 - len(s) % 3) + s
    return ''.join(chr(int(s[i:i+3])) for i in range(0, len(s), 3))

# === MAIN PROGRAM ===
print("=== RSA Setup ===")
try:
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))

    # Validate primes
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("❌ Both p and q must be prime numbers.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = int(input("Enter public exponent e (1 < e < φ(n), and gcd(e, φ(n)) = 1): "))

    # Validate e
    if not (1 < e < phi):
        raise ValueError("❌ e must be greater than 1 and less than φ(n).")
    from math import gcd
    if gcd(e, phi) != 1:
        raise ValueError("❌ e must be co-prime with φ(n).")

    # Compute private key d
    d = mod_inverse(e, phi)

    print(f"\n✅ Public Key  (e, n): ({e}, {n})")
    print(f"🔐 Private Key (d, n): ({d}, {n})")

    # Message input
    plaintext = input("\nEnter plaintext message: ")

    # Optional: Limit characters to ASCII (0–126)
    for c in plaintext:
        if ord(c) > 126:
            raise ValueError(f"❌ Unsupported character detected: {c}")

    M = text_to_number(plaintext)

    # Validation: M must be smaller than n
    if M >= n:
        raise ValueError("❌ Message is too long. Try using larger primes or shorter message.")

    # Encrypt
    C = encrypt(M, e, n)
    print(f"\n🔒 Encrypted numeric message: {C}")

    # Decrypt
    M_decrypted = decrypt(C, d, n)
    decrypted_text = number_to_text(M_decrypted)

    # Final output
    print(f"🔓 Decrypted numeric message: {M_decrypted}")
    print(f"📩 Decrypted plaintext message: {decrypted_text}")

except Exception as err:
    print(f"🚫 Error: {err}")
