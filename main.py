from sympy import mod_inverse

# secp256k1 params
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

# Generator point G
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

# Elliptic curve point addition and doubling
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    if P == Q:
        # Point doubling
        s = (3 * P[0]**2 + a) * mod_inverse(2 * P[1], p) % p
    else:
        if P[0] == Q[0]:
            return None  # Point at infinity
        s = (Q[1] - P[1]) * mod_inverse(Q[0] - P[0], p) % p

    Rx = (s**2 - P[0] - Q[0]) % p
    Ry = (s * (P[0] - Rx) - P[1]) % p
    return (Rx, Ry)

def point_neg(P):
    if P is None:
        return None
    return (P[0], (-P[1]) % p)

def point_sub(P, Q):
    return point_add(P, point_neg(Q))

def point_mul(k, P):
    R = None
    addend = P
    while k:
        if k & 1:
            R = point_add(R, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return R

# Find points of order 3 by brute force in a limited range
def find_order_3_points(limit=50000):
    order3_points = []
    for x_candidate in range(1, limit):
        rhs = (pow(x_candidate, 3, p) + b) % p
        legendre = pow(rhs, (p - 1) // 2, p)
        if legendre == 1:
            # Tonelli-Shanks shortcut since p % 4 == 3
            y_candidate = pow(rhs, (p + 1) // 4, p)
            P = (x_candidate, y_candidate)
            P2 = point_add(P, P)
            P3 = point_add(P2, P)
            if P3 is None:  # 3P = O
                order3_points.append(P)
    return order3_points

# Vélu's degree-3 isogeny map
def velu_degree_3_isogeny(P, kernel_point):
    P1 = kernel_point
    P2 = point_add(P1, P1)

    xP, yP = P
    numerator_x = 0
    numerator_y = 0

    for Q in [P1, P2]:
        denom = (xP - Q[0]) % p
        if denom == 0:
            return None
        inv_denom = mod_inverse(denom, p)
        numerator_x += (Q[0] * inv_denom) % p
        numerator_y += (Q[1] * inv_denom) % p

    numerator_x %= p
    numerator_y %= p

    x_phiP = (xP + numerator_x) % p
    y_phiP = (yP + numerator_y) % p

    return (x_phiP, y_phiP)

if __name__ == "__main__":
    print("Searching order-3 points (this might take a while)...")
    kernel3 = find_order_3_points()
    print(f"Found order-3 kernel points: {len(kernel3)}")

    if kernel3:
        mappedG = velu_degree_3_isogeny((Gx, Gy), kernel3[0])
        print(f"Mapped G via degree-3 isogeny: {mappedG}")
    else:
        print("No order-3 points found in range.")