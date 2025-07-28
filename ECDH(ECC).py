# Elliptic Curve Diffie-Hellman Key Exchange

p = 13
a = 1
b = 2
G = (7, 1)
n = 12

def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None

    if P == Q:
        m = ((3 * x1**2 + a) * inverse_mod(2 * y1, p)) % p
    else:
        m = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_mult(k, P):
    result = None
    addend = P

    while k > 0:
        if k % 2 == 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k = k // 2

    return result

def is_on_curve(P):
    if P is None:
        return True
    x, y = P
    return (y * y - (x**3 + a * x + b)) % p == 0

def has_order_n(P, n):
    return scalar_mult(n, P) is None

# Validate base point
if not is_on_curve(G):
    raise ValueError(f"Base point G={G} is not on the curve.")
if not has_order_n(G, n):
    raise ValueError(f"Base point G={G} does not have order {n}.")

# Input private keys
alpha = int(input("Enter Alline's private key (α): "))
beta = int(input("Enter Bose's private key (β): "))

if not (1 <= alpha < n):
    raise ValueError("Invalid α. Must be in range [1, n-1]")
if not (1 <= beta < n):
    raise ValueError("Invalid β. Must be in range [1, n-1]")

# Compute public keys
Pa = scalar_mult(alpha, G)
Pb = scalar_mult(beta, G)

# Validate public keys
if not is_on_curve(Pa):
    raise ValueError(f"Public key Pa={Pa} is not on the curve.")
if not is_on_curve(Pb):
    raise ValueError(f"Public key Pb={Pb} is not on the curve.")

# Compute shared secrets
K_alline = scalar_mult(alpha, Pb)
K_bose = scalar_mult(beta, Pa)

# Output
print(f"\nElliptic Curve: y^2 = x^3 + {a}x + {b} mod {p}")
print("Base Point G:", G)
print("Order n:", n)

print("\n-- Alline --")
print("Private Key α:", alpha)
print("Public Key Pa:", Pa)

print("\n-- Bose --")
print("Private Key β:", beta)
print("Public Key Pb:", Pb)

print("\n-- Shared Secret Key --")
print("K (computed by Alline):", K_alline)
print("K (computed by Bose):  ", K_bose)
