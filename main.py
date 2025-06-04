from sympy import mod_inverse
import random

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    if P == Q:
        if P[1] == 0:
            return None
        s = (3 * P[0] ** 2 + a) * mod_inverse(2 * P[1], p) % p
    else:
        if P[0] == Q[0]:
            return None
        s = (Q[1] - P[1]) * mod_inverse(Q[0] - P[0], p) % p

    Rx = (s ** 2 - P[0] - Q[0]) % p
    Ry = (s * (P[0] - Rx) - P[1]) % p
    return (Rx, Ry)

def point_neg(P):
    return (P[0], (-P[1]) % p) if P else None

def point_mul(k, P):
    R = None
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k = k // 2
    return R

def is_on_curve(P):
    if P is None:
        return False
    x, y = P
    return (y ** 2 - (x ** 3 + a * x + b)) % p == 0

def find_order_3_points(limit=100000):
    found = []
    tries = 0
    print("Searching for order-3 points...")
    while len(found) < 1 and tries < limit:
        x = random.randint(1, p - 1)
        rhs = (x ** 3 + b) % p
        y2 = pow(rhs, (p + 1) // 4, p)
        if pow(y2, 2, p) != rhs:
            tries += 1
            continue
        P = (x, y2)
        if not is_on_curve(P):
            tries += 1
            continue
        P3 = point_mul(3, P)
        if P3 is None:
            print(f"✅ Found order-3 point at x = {x}")
            found.append(P)
        tries += 1
    print(f"Total found: {len(found)} after {tries} tries")
    return found

if __name__ == "__main__":
    order3_points = find_order_3_points(500000)
    for idx, pt in enumerate(order3_points):
        print(f"Order-3 Point #{idx+1}: {pt}")