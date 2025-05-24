from ecdsa import ellipticcurve, SECP256k1

# Curve and generator
curve = SECP256k1.curve
G = SECP256k1.generator
n = SECP256k1.order

# Given scalar
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
        print("Invalid input or point:", e)
        return None

def main():
    Q = get_public_key()
    if Q is None:
        return

    # Compute Q*2 + 2G + d*G
    expr1 = Q * 2 + G * 2 + G * d
    print("First x-coordinate (hex):", hex(expr1.x()))

    # Compute d*G
    dG = G * d  # This is a PointJacobi
    dG_affine = dG.to_affine()  # Convert to affine Point

    # Convert Q to PointJacobi temporarily to match types
    Q_jacobi = dG_affine.__class__.from_affine(Q)

    # Now compute (d*G - Q)
    dG_minus_Q = dG - Q_jacobi  # both PointJacobi

    # Final expression: dG + (dG - Q) + Q
    result = dG + dG_minus_Q + Q_jacobi
    x2 = result.to_affine().x()
    print("Second x-coordinate (hex):", hex(x2))

    if expr1.x() == x2:
        print("your d < n/2")
    else:
        print("Mismatch or incorrect point")

if __name__ == "__main__":
    main()