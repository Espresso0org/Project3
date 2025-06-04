import random
import time

# === Utility Functions ===

def is_prime(n, k=5):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def is_on_curve(P, a, b, p):
    if P is None:
        return True
    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    if P == Q:
        return point_double(P, a, p)
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return None
    lam = ((Q[1] - P[1]) * pow(Q[0] - P[0], -1, p)) % p
    x_r = (lam * lam - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

def point_double(P, a, p):
    if P is None:
        return None
    x, y = P
    lam = ((3 * x * x + a) * pow(2 * y, -1, p)) % p
    x_r = (lam * lam - 2 * x) % p
    y_r = (lam * (x - x_r) - y) % p
    return (x_r, y_r)

def point_mul(P, d, a, p):
    R = None
    addend = P
    while d > 0:
        if d & 1:
            R = point_add(R, addend, a, p)
        addend = point_double(addend, a, p)
        d >>= 1
    return R

def pollards_rho_dlp(G, Q, n, a, p):
    def f(X, a_i, b_i):
        x, y = X
        if x % 3 == 0:
            X = point_add(X, G, a, p)
            a_i = (a_i + 1) % n
        elif x % 3 == 1:
            X = point_add(X, Q, a, p)
            b_i = (b_i + 1) % n
        else:
            X = point_double(X, a, p)
            a_i = (2 * a_i) % n
            b_i = (2 * b_i) % n
        return X, a_i, b_i

    x = random.randint(1, n-1)
    a_i = x
    b_i = 0
    X = point_mul(G, x, a, p)
    x2, a2, b2 = X, a_i, b_i

    for _ in range(n * 2):
        X, a_i, b_i = f(X, a_i, b_i)
        x2, a2, b2 = f(*f(x2, a2, b2))

        if X == x2:
            r = (a_i - a2) % n
            s = (b2 - b_i) % n
            if s == 0:
                return None
            inv = pow(s, -1, n)
            return (r * inv) % n
    return None

def inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def crt(remainders, moduli):
    total = 0
    prod = 1
    for m in moduli: prod *= m
    for r, m in zip(remainders, moduli):
        p = prod // m
        inv = inverse(p, m)
        total += r * inv * p
    return total % prod

# === Test Script ===

def generate_small_curve(bits=28):
    while True:
        p = random.getrandbits(bits) | 1
        if is_prime(p):
            a = random.randint(1, p - 1)
            b = random.randint(1, p - 1)
            return p, a, b

def test_mapping_and_recovery(d_known, trials=6, bits=28):
    print(f"Starting full test for d = {d_known}")

    # secp256k1 parameters
    secp_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    secp_a = 0
    secp_b = 7
    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    G = (Gx, Gy)

    Q_big = point_mul(G, d_known, secp_a, secp_p)
    print(f"Generated Q_big from d_known: {Q_big}\n")

    remainders = []
    moduli = []

    for i in range(trials):
        print(f"--- Curve #{i+1} ---")
        p, a, b = generate_small_curve(bits)
        print(f"Curve: p={p}, a={a}, b={b}")

        Q_small = (Q_big[0] % p, Q_big[1] % p)
        if not is_on_curve(Q_small, a, b, p):
            print("Mapped Q is NOT on curve. Skipping.\n")
            continue

        print("Mapped Q is ON the small curve.")
        start = time.time()
        d_mod = pollards_rho_dlp(G, Q_small, p, a, p)
        if d_mod is None:
            print("Pollard’s Rho failed.\n")
            continue

        Q_check = point_mul(G, d_mod, a, p)
        if Q_check != Q_small:
            print("Verification failed: computed Q doesn't match mapped Q. Skipping.\n")
            continue

        print(f"Success: d mod p = {d_mod}, verified in {time.time() - start:.2f}s\n")
        remainders.append(d_mod)
        moduli.append(p)

    if not remainders:
        print("No valid results collected. Test failed.")
        return

    d_recovered = crt(remainders, moduli)
    mod_product = 1
    for m in moduli: mod_product *= m

    print(f"\n--- Final Result ---")
    print(f"Reconstructed d (mod product): {d_recovered}")
    print(f"d_known mod product: {d_known % mod_product}")

    if d_recovered == d_known % mod_product:
        print("✅ SUCCESS: Private key recovery verified.")
    else:
        print("❌ FAILURE: Recovered key doesn't match.")

if __name__ == "__main__":
    test_mapping_and_recovery(d_known=123456789)