import random

# Modular inverse function
def inv_mod(k, p):
    return pow(k, p-2, p)

# Elliptic curve point addition
def point_add(P, Q, a, p):
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return (None, None)
    if P == Q:
        lam = (3 * P[0] * P[0] + a) * inv_mod(2 * P[1], p) % p
    else:
        lam = (Q[1] - P[1]) * inv_mod(Q[0] - P[0], p) % p
    x = (lam * lam - P[0] - Q[0]) % p
    y = (lam * (P[0] - x) - P[1]) % p
    return (x, y)

# Elliptic curve scalar multiplication
def point_mul(k, P, a, p):
    R = (None, None)
    addend = P
    while k > 0:
        if k & 1:
            R = point_add(R, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return R

# Pollard's Rho discrete log in subgroup order
def pollards_rho(P, Q, a, p, order):
    def f(X, aX, bX):
        x, y = X
        if x % 3 == 0:
            X_new = point_add(X, P, a, p)
            return X_new, (aX + 1) % order, bX
        elif x % 3 == 1:
            X_new = point_add(X, Q, a, p)
            return X_new, aX, (bX + 1) % order
        else:
            X_new = point_add(X, X, a, p)
            return X_new, (2 * aX) % order, (2 * bX) % order

    x, aX, bX = P, 1, 0
    X, aX2, bX2 = P, 1, 0
    for _ in range(1, order):
        x, aX, bX = f(x, aX, bX)
        X, aX2, bX2 = f(*f(X, aX2, bX2))
        if x == X:
            r = (bX - bX2) % order
            if r == 0:
                return None
            inv_r = inv_mod(r, order)
            d = (aX2 - aX) * inv_r % order
            return d
    return None

# Extended Euclidean for CRT
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, y, x = egcd(b, a % b)
    return g, x, y - (a // b) * x

def crt(congruences):
    x = 0
    M = 1
    for _, modulus in congruences:
        M *= modulus
    for residue, modulus in congruences:
        m = M // modulus
        g, inv, _ = egcd(m, modulus)
        if g != 1:
            return None
        x = (x + residue * inv * m) % M
    return x, M

# secp256k1 parameters
p_big = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a_big = 0
b_big = 7
G_big = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
         32670510020758816978083085130507043184471273380659243275938904335757337482424)
n_big = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Generate random private key
d_test = random.randint(1, n_big - 1)
Q_big = point_mul(d_test, G_big, a_big, p_big)

print(f"Test private key d: {d_test}")
print(f"Public key Q: {Q_big}")

# Small prime factors of n_big (subset for demo)
prime_factors = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

congruences = []

for p_i in prime_factors:
    m = n_big // p_i
    G_i = point_mul(m, G_big, a_big, p_big)
    Q_i = point_mul(m, Q_big, a_big, p_big)

    if G_i == (None, None) or Q_i == (None, None):
        print(f"Skipping trivial subgroup for prime {p_i}")
        continue

    print(f"Solving DLP mod {p_i}...")

    d_i = pollards_rho(G_i, Q_i, a_big, p_big, p_i)
    if d_i is None:
        print(f"Failed to solve DLP mod {p_i}")
        continue

    print(f"d mod {p_i} = {d_i}")
    congruences.append((d_i, p_i))

if congruences:
    d_recovered, mod_product = crt(congruences)
    print(f"Recovered d mod product: {d_recovered} mod {mod_product}")

    Q_recovered = point_mul(d_recovered, G_big, a_big, p_big)
    if Q_recovered == Q_big:
        print("SUCCESS: Recovered private key matches public key")
    else:
        print("FAILURE: Recovered private key does NOT match public key")
else:
    print("No DLP solutions found; recovery failed.")