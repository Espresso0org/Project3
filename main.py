from hashlib import sha256

# Curve parameters for secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def inv_mod(k, p):
    return pow(k, p-2, p)

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        if P[1] == 0:
            return None
        s = (3 * P[0] * P[0] * inv_mod(2 * P[1], p)) % p
    else:
        if P[0] == Q[0]:
            return None
        s = ((Q[1] - P[1]) * inv_mod(Q[0] - P[0], p)) % p
    Rx = (s * s - P[0] - Q[0]) % p
    Ry = (s * (P[0] - Rx) - P[1]) % p
    return (Rx, Ry)

def point_double(P):
    return point_add(P, P)

def scalar_mult(k, P, fault_bit=None):
    R = None
    Q = P
    for i in reversed(range(k.bit_length())):
        R = point_double(R)
        bit = (k >> i) & 1
        # Simulate fault by flipping the bit at fault_bit position
        if i == fault_bit:
            bit = 1 - bit
        if bit == 1:
            R = point_add(R, Q)
    return R

def points_equal(P, Q):
    return P == Q

def print_point(label, P):
    if P is None:
        print(f"{label}: Point at infinity")
    else:
        print(f"{label}: (0x{P[0]:x}, 0x{P[1]:x})")

if __name__ == "__main__":
    import random

    # Example private key d (random 256-bit)
    d = random.randint(1, n-1)

    G = (Gx, Gy)
    Q = scalar_mult(d, G)  # Correct public key

    print_point("Correct Q", Q)
    print(f"Private key d: {d}")

    # Try faults at each bit of d
    for fault_bit in range(d.bit_length()):
        Q_faulty = scalar_mult(d, G, fault_bit=fault_bit)
        diff = not points_equal(Q, Q_faulty)
        print(f"Fault at bit {fault_bit}: {'DIFFERENT' if diff else 'SAME'}")
        if diff:
            print_point("Faulty Q", Q_faulty)