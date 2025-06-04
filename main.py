import random
import math

# Elliptic curve point operations over prime field
def inv_mod(k, p):
    return pow(k, p-2, p)

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

def point_mul(k, P, a, p):
    R = (None, None)
    addend = P
    while k > 0:
        if k & 1:
            R = point_add(R, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return R

# Pollard's Rho for discrete log on elliptic curve
def pollards_rho(P, Q, a, p, order):
    # Random function parameters
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

# Check point on curve
def is_on_curve(P, a, b, p):
    if P == (None, None):
        return True
    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0

# Extended Euclidean algorithm for CRT
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

# Generate random small prime for test
def small_primes():
    # A fixed list of small primes for curves
    return [101, 103, 107, 109, 113, 127, 131, 137]

# Parameters for secp256k1 for original curve (for verification)
p_big = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a_big = 0
b_big = 7
G_big = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
         32670510020758816978083085130507043184471273380659243275938904335757337482424)
n_big = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Generate secret d and public key Q on big curve
d_test = random.randint(1, n_big - 1)
Q_big = point_mul(d_test, G_big, a_big, p_big)

print(f"Secret d_test (hidden in real attack): {d_test}")
print(f"Public key Q_big: {Q_big}")

# Define small curves with parameters (for test)
# We use curves y^2 = x^3 + a x + b mod p with small prime p
small_curves = []
for p in small_primes():
    a = random.randint(0, p - 1)
    b = random.randint(0, p - 1)
    # Try to find a generator point G on curve
    G = None
    for x_try in range(p):
        rhs = (x_try ** 3 + a * x_try + b) % p
        # check if rhs is quadratic residue mod p
        # simple check by Euler's criterion:
        if pow(rhs, (p - 1) // 2, p) == 1:
            # find y
            y_try = pow(rhs, (p + 1) // 4, p)
            G = (x_try, y_try)
            if is_on_curve(G, a, b, p):
                break
    if G is None:
        continue
    order = p  # approximate order as p for test
    small_curves.append((p, a, b, G, order))

print(f"Number of small curves found: {len(small_curves)}")

# For each small curve, try to find mapping and solve discrete log
congruences = []
for (p, a, b, G, order) in small_curves:
    Qx_mod = Q_big[0] % p
    Qy_mod = Q_big[1] % p

    # Find k in [1..order] such that k*G = Q_mod (if exists)
    found = False
    for k in range(1, order):
        P = point_mul(k, G, a, p)
        if P == (Qx_mod, Qy_mod):
            print(f"Curve mod {p}: Found k = {k}")
            congruences.append((k, p))
            found = True
            break
    if not found:
        print(f"Curve mod {p}: No match found")

# Apply CRT on all found congruences
if congruences:
    d_recovered, mod_product = crt(congruences)
    print(f"Recovered d mod product({[c[1] for c in congruences]}) = {d_recovered}")

    # Verify recovered key on big curve
    Q_recovered = point_mul(d_recovered, G_big, a_big, p_big)
    if Q_recovered == Q_big:
        print("SUCCESS: Recovered private key matches public key")
    else:
        print("FAILURE: Recovered key does not match public key")
else:
    print("No partial keys recovered from small curves")