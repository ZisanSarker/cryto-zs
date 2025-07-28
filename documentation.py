"""
Elliptic Curve Diffie-Hellman (ECDH) Key Exchange

ECDH is a public-key cryptographic protocol that allows two parties to 
establish a shared secret over an insecure channel using elliptic curve cryptography.

Key Concepts:
-------------
- Elliptic Curve: A curve defined by the equation y^2 = x^3 + a*x + b (mod p)
  where 'p' is a prime modulus defining the finite field.

- Base Point (G): A predefined point on the elliptic curve used as a generator 
  for scalar multiplication. It has a prime order 'n' such that n*G = O (point at infinity).

- Private Key (α or β): A randomly selected integer in the range [1, n-1]. Kept secret.

- Public Key (Pa or Pb): The result of scalar multiplication of the base point by 
  the private key: Pa = α*G, Pb = β*G. Publicly shared.

- Shared Secret (K): Both parties compute K by multiplying the other party's public key
  by their own private key: K = α*Pb = β*Pa. Due to properties of elliptic curves,
  both compute the same point K, which can be used as a shared secret key.

Procedure:
----------
1. Agree on common elliptic curve parameters (p, a, b), base point G, and order n.

2. Each party generates a private key α or β, a secret integer in [1, n-1].

3. Each computes their public key by scalar multiplication of G by their private key.

4. The parties exchange public keys over the insecure channel.

5. Each computes the shared secret by scalar multiplying their private key with the received public key.

6. The shared secret point coordinates can be further processed (e.g., hashing) to derive symmetric encryption keys.

Security:
---------
ECDH security relies on the hardness of the Elliptic Curve Discrete Logarithm Problem (ECDLP):
Given G and α*G, it is computationally infeasible to determine α.

This enables secure key agreement without exposing private keys or the shared secret during communication.

This implementation:
--------------------
- Uses a small example curve over a finite field defined by prime p = 13.
- Includes point addition and scalar multiplication functions.
- Validates points to ensure correctness.
- Takes private keys as input and computes shared secret.
- Intended for educational/demonstration purposes and not for production use.

"""
#===========================================================================================================
