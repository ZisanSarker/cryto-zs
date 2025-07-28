#Elliptic Curve Integrated Encryption Scheme (ECIES)

import random

# Elliptic Curve Parameters
p = 13
a = 1
b = 2
G = (7, 1)
n = 12

# Modular inverse
def inverse_mod(k, p):
    return pow(k, -1, p)

# Point addition
def point_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None

    if P == Q:
        m = ((3 * x1**2 + a) * inverse_mod(2 * y1, p)) % p
    else:
        m = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

# Scalar multiplication
def scalar_mul(k, P):
    result = None
    addend = P
    while k > 0:
        if k % 2 == 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k //= 2
    return result

# ECIES Encryption
def ecies_encrypt(msg, Pb):
    r = random.randint(1, n - 1)
    R = scalar_mul(r, G)
    S = scalar_mul(r, Pb)
    k = S[0] % 256
    cipher = [ord(c) ^ k for c in msg]
    return R, cipher

# ECIES Decryption
def ecies_decrypt(R, cipher, b):
    S = scalar_mul(b, R)
    k = S[0] % 256
    msg = ''.join([chr(c ^ k) for c in cipher])
    return msg

# --- Main Execution ---

# Generate receiver keys (Bob)
b = int(input("Enter Bob's private key (1 to n-1): "))
if not (1 <= b < n):
    raise ValueError("Private key must be in range 1 to n-1")

Pb = scalar_mul(b, G)
print("Bob's public key Pb:", Pb)

# Encrypt
message = input("Enter message to encrypt (plaintext): ")
R, cipher = ecies_encrypt(message, Pb)

print("\n--- Encrypted ---")
print("Ciphertext (ASCII codes):", cipher)
# print("Ciphertext (characters) :", ''.join(chr(c) for c in cipher))
print("Ephemeral public key (R):", R)

# Decrypt
decrypted = ecies_decrypt(R, cipher, b)
print("\n--- Decrypted ---")
print("Decrypted message:", decrypted)
