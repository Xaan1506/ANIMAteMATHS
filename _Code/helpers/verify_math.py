#!/usr/bin/env python3
"""NumPy verification of all Gaussian elimination steps and final solution."""
import numpy as np

def verify():
    print("=" * 60)
    print("NUMPY VERIFICATION — Gaussian Elimination")
    print("=" * 60)

    # Original system
    A = np.array([[1, 1, 1],
                  [2, 3, 1],
                  [1, 2, 3]], dtype=float)
    b = np.array([6, 11, 14], dtype=float)
    aug = np.column_stack([A, b])
    print(f"\nOriginal augmented matrix:\n{aug}")

    # Step 1: R2 → R2 - 2*R1
    aug[1] = aug[1] - 2 * aug[0]
    print(f"\nAfter R2 ← R2 - 2R1:\n{aug}")
    expected_r2 = np.array([0, 1, -1, -1], dtype=float)
    assert np.allclose(aug[1], expected_r2), f"Step 1 FAILED: {aug[1]} != {expected_r2}"
    print("  ✓ Step 1 correct")

    # Step 2: R3 → R3 - R1
    aug[2] = aug[2] - aug[0]
    print(f"\nAfter R3 ← R3 - R1:\n{aug}")
    expected_r3 = np.array([0, 1, 2, 8], dtype=float)
    assert np.allclose(aug[2], expected_r3), f"Step 2 FAILED: {aug[2]} != {expected_r3}"
    print("  ✓ Step 2 correct")

    # Step 3: R3 → R3 - R2
    aug[2] = aug[2] - aug[1]
    print(f"\nAfter R3 ← R3 - R2:\n{aug}")
    expected_r3_final = np.array([0, 0, 3, 9], dtype=float)
    assert np.allclose(aug[2], expected_r3_final), f"Step 3 FAILED: {aug[2]} != {expected_r3_final}"
    print("  ✓ Step 3 correct")

    # Final REF
    print(f"\nRow Echelon Form:\n{aug}")

    # Back substitution
    z = aug[2, 3] / aug[2, 2]  # 9/3 = 3
    y = (aug[1, 3] - aug[1, 2] * z) / aug[1, 1]  # (-1 - (-1)*3)/1 = 2
    x = (aug[0, 3] - aug[0, 2] * z - aug[0, 1] * y) / aug[0, 0]  # (6 - 3 - 2)/1 = 1

    print(f"\nBack substitution:")
    print(f"  3z = 9  →  z = {z}")
    print(f"  y - z = -1  →  y - 3 = -1  →  y = {y}")
    print(f"  x + y + z = 6  →  x + 2 + 3 = 6  →  x = {x}")
    print(f"\nSolution: (x, y, z) = ({x}, {y}, {z})")

    assert x == 1.0, f"x should be 1, got {x}"
    assert y == 2.0, f"y should be 2, got {y}"
    assert z == 3.0, f"z should be 3, got {z}"
    print("  ✓ Solution correct")

    # Verify by substitution into original equations
    print("\nVerification by substitution:")
    eq1 = x + y + z
    eq2 = 2*x + 3*y + z
    eq3 = x + 2*y + 3*z
    print(f"  x + y + z = {eq1} (expected 6) {'✓' if eq1 == 6 else '✗'}")
    print(f"  2x + 3y + z = {eq2} (expected 11) {'✓' if eq2 == 11 else '✗'}")
    print(f"  x + 2y + 3z = {eq3} (expected 14) {'✓' if eq3 == 14 else '✗'}")

    assert eq1 == 6 and eq2 == 11 and eq3 == 14, "Substitution verification FAILED"

    # Also verify using numpy.linalg.solve
    A_orig = np.array([[1, 1, 1], [2, 3, 1], [1, 2, 3]], dtype=float)
    b_orig = np.array([6, 11, 14], dtype=float)
    solution = np.linalg.solve(A_orig, b_orig)
    print(f"\nnp.linalg.solve result: {solution}")
    assert np.allclose(solution, [1, 2, 3]), "np.linalg.solve verification FAILED"
    print("  ✓ np.linalg.solve confirms (1, 2, 3)")

    print("\n" + "=" * 60)
    print("ALL VERIFICATIONS PASSED ✓")
    print("=" * 60)
    return True

if __name__ == "__main__":
    verify()
