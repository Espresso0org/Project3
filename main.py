from sympy import mod_inverse

# Curve params for secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

# Generator point G (x, y)
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

# Elliptic curve point addition and doubling over F_p
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    if P == Q:
        # point doubling
        s = (3 * P[0]**2 + a) * mod_inverse(2 * P[1], p) % p
    else:
        if P[0] == Q[0]:
            return None
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

# Vélu's formulas for degree-2 isogeny
def velu_isogeny(P, kernel_points):
    # P: point to map
    # kernel_points: list of points forming kernel subgroup (excluding O)

    # Sum over kernel points
    Sx = 0
    Sy = 0

    for Q in kernel_points:
        if Q is None:
            continue
        xQ, yQ = Q
        # Compute terms for Vélu's formula
        denom = (P[0] - xQ) % p
        if denom == 0:
            # P coincides with kernel point -> map to point at infinity
            return None

        inv_denom = mod_inverse(denom, p)
        Sx += (xQ * inv_denom) % p
        Sy += (yQ * inv_denom) % p

    Sx %= p
    Sy %= p

    xP, yP = P

    # New coordinates on the isogenous curve
    x_phiP = (xP + Sx) % p
    y_phiP = (yP + Sy) % p

    return (x_phiP, y_phiP)

# Example: build kernel subgroup for degree-2 isogeny (order 2 point)
def find_order_2_points():
    # Search for points of order 2 (2P=O) on secp256k1
    # Points where y=0 satisfy 2P=O on curves y^2=x^3+ax+b
    order2_points = []
    for x_candidate in range(1, 1000):
        rhs = (x_candidate**3 + a*x_candidate + b) % p
        if pow(rhs, (p-1)//2, p) == 1:
            # Check if y=0 is a solution: y^2 = rhs, y=0 => 0 = rhs => rhs == 0 mod p
            if rhs == 0:
                order2_points.append((x_candidate, 0))
    return order2_points

print("Finding order-2 points...")
kernel = find_order_2_points()
print(f"Kernel subgroup candidates (order 2): {kernel}")

# Testing isogeny map on G
if kernel:
    print("Applying Vélu's isogeny to G...")
    G_mapped = velu_isogeny((Gx, Gy), kernel)
    print(f"Mapped G: {G_mapped}")
else:
    print("No order-2 points found; degree-2 isogeny not possible.")