def power_mod(base, exponent, modulus):
    """Efficient modular exponentiation: (base^exponent) % modulus"""
    return pow(base, exponent, modulus)

def is_prime(n):
    """Check if a number is prime (basic check)"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

def is_primitive_root(g, p):
    """Check if g is a primitive root modulo p"""
    required_set = set(range(1, p))
    actual_set = set()

    for i in range(1, p):
        actual_set.add(power_mod(g, i, p))
    
    return required_set == actual_set

# 1. Publicly shared prime and generator
while True:
    p = int(input("🔢 Enter a prime number (p): "))
    if is_prime(p):
        break
    print("❌ Invalid input: p must be a prime number.")

while True:
    g = int(input("⚙️  Enter a primitive root modulo p (g): "))
    if 1 <= g < p and is_primitive_root(g, p):
        break
    print(f"❌ {g} is not a primitive root modulo {p}. Try another.")

# 2. Alice's private key
while True:
    a = int(input("\n🧑‍💼 Enter Alice's private key (a): "))
    if 1 <= a < p:
        break
    print(f"❌ Invalid private key. It must be in the range 1 to {p-1}.")

A = power_mod(g, a, p)  # Alice's public key

# 3. Bob's private key
while True:
    b = int(input("\n🧑‍🔧 Enter Bob's private key (b): "))
    if 1 <= b < p:
        break
    print(f"❌ Invalid private key. It must be in the range 1 to {p-1}.")

B = power_mod(g, b, p)  # Bob's public key

# 4. Exchange and compute shared secrets
shared_secret_alice = power_mod(B, a, p)
shared_secret_bob = power_mod(A, b, p)

# 5. Output results
print("\n📡 Public Prime (p):", p)
print("📡 Generator (g):", g)

print("\n🔐 Alice's Public Key (A = g^a mod p):", A)
print("🔐 Bob's Public Key (B = g^b mod p):", B)

print("\n🧮 Shared Secret (computed by Alice):", shared_secret_alice)
print("🧮 Shared Secret (computed by Bob):", shared_secret_bob)

# 6. Validation
if shared_secret_alice == shared_secret_bob:
    print("\n✅ Key exchange successful! Shared secret =", shared_secret_alice)
else:
    print("\n❌ Key exchange failed. Shared secrets do not match.")
