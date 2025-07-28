def power_mod(base, exponent, modulus):
    """Efficient modular exponentiation: (base^exponent) % modulus"""
    return pow(base, exponent, modulus)

# 1. Publicly shared prime and generator
p = int(input("🔢 Enter a prime number (p): "))
g = int(input("⚙️  Enter a primitive root modulo p (g): "))

# 2. Alice's private key
a = int(input("\n🧑‍💼 Enter Alice's private key (a): "))
A = power_mod(g, a, p)  # Alice's public key

# 3. Bob's private key
b = int(input("\n🧑‍🔧 Enter Bob's private key (b): "))
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
