import random

# Curve parameters
p = 13
a = 1
b = 2
G = (7, 1)
n = 12

def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None
    if P == Q:
        m = ((3*x1**2 + a)*inverse_mod(2*y1, p)) % p
    else:
        m = ((y2 - y1)*inverse_mod(x2 - x1, p)) % p
    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P):
    result = None
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def encode_message(m):
    # Encode integer m as a point on curve (assume 0 <= m < p)
    for y in range(p):
        if (y*y) % p == (m**3 + a*m + b) % p:
            return (m, y)
    return None

def decode_message(P):
    if P is None:
        return None
    return P[0]

def elgamal_encrypt(M, Pb):
    k = random.randint(1, n-1)
    C1 = scalar_mul(k, G)
    C2 = point_add(M, scalar_mul(k, Pb))
    return C1, C2

def elgamal_decrypt(C1, C2, b):
    S = scalar_mul(b, C1)
    S_inv = (S[0], (-S[1]) % p) if S is not None else None
    M = point_add(C2, S_inv)
    return M

# --- Main ---

b = int(input("Enter private key b (1 to n-1): "))
if not (1 <= b < n):
    raise ValueError("Private key out of range")

Pb = scalar_mul(b, G)
print("Public key Pb:", Pb)

m = int(input(f"Enter message integer m (0 to {p-1}): "))
M = encode_message(m)
if M is None:
    raise ValueError(f"Cannot encode message {m} as point on curve")

C1, C2 = elgamal_encrypt(M, Pb)
print("Ciphertext:")
print("C1:", C1)
print("C2:", C2)

M_dec = elgamal_decrypt(C1, C2, b)
m_dec = decode_message(M_dec)
print("Decrypted message integer:", m_dec)
