from ecdsa import ellipticcurve, SECP256k1

# Use secp256k1 curve
curve = SECP256k1.curve
G = SECP256k1.generator
n = SECP256k1.order

# Your scalar
d = 0x7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0

def get_public_key():
    x_hex = input("Enter the X coordinate of the public key (hex): ").strip()
    y_hex = input("Enter the Y coordinate of the public key (hex): ").strip()
    try:
        x = int(x_hex, 16)
        y = int(y_hex, 16)
        Q = ellipticcurve.Point(curve, x, y)
        return Q
    except Exception as e:
        print("Invalid point:", e)
        return None

def main():
    Q = get_public_key()
    if Q is None:
        return

    # All points are affine here, no PointJacobi!
    Q2 = Q * 2
    G2 = G * 2
    dG = G * d

    # First expression
    expr1 = Q2 + G2 + dG
    print("First x-coordinate (hex):", hex(expr1.x()))

    # Second expression
    dG_minus_Q = ellipticcurve.Point(curve, dG.x(), dG.y()) - Q  # force affine
    expr2 = dG + dG_minus_Q + Q
    print("Second x-coordinate (hex):", hex(expr2.x()))

    # Compare results
    if expr1.x() == expr2.x():
        print("your d < n/2")
    else:
        print("Mismatch or incorrect point")

if __name__ == "__main__":
    main()