# Viva Preparation — Gaussian Elimination Animation

**Student:** Gyanam (E25B070726)

---

## 15 Likely Viva Questions and Answers

### Q1: What is Gaussian elimination?

**A:** Gaussian elimination is a systematic algorithm that transforms a system of linear equations into row echelon form using elementary row operations, after which back substitution reveals the unknowns. It was named after Carl Friedrich Gauss.

---

### Q2: What are the three elementary row operations?

**A:**
1. **Swap** two rows.
2. **Scale** a row by multiplying every entry by a non-zero scalar.
3. **Replace** a row by adding a scalar multiple of another row to it.

---

### Q3: Why do row operations preserve the solution set?

**A:** Each row operation produces an equivalent system — one with the same set of solutions. Swapping rows is just reordering equations. Scaling multiplies both sides by the same non-zero number. Adding a multiple of one equation to another combines valid equalities, which preserves all solutions.

---

### Q4: What is the difference between REF and RREF?

**A:** In **Row Echelon Form (REF)**, each leading entry (pivot) is to the right of the pivot above, and all entries below each pivot are zero. In **Reduced Row Echelon Form (RREF)**, every pivot is additionally equal to 1 and all entries *above* each pivot are also zero. RREF requires extra work but yields the solution directly without back substitution.

---

### Q5: Walk through the row operations you performed.

**A:**
- **Step 1:** R₂ ← R₂ − 2R₁ → Eliminated the x-coefficient in row 2, giving [0, 1, −1 | −1].
- **Step 2:** R₃ ← R₃ − R₁ → Eliminated the x-coefficient in row 3, giving [0, 1, 2 | 8].
- **Step 3:** R₃ ← R₃ − R₂ → Eliminated the y-coefficient in row 3, giving [0, 0, 3 | 9].

---

### Q6: How did you verify the solution (1, 2, 3)?

**A:** I substituted back into all three original equations:
- 1 + 2 + 3 = 6 ✓
- 2(1) + 3(2) + 3 = 11 ✓
- 1 + 2(2) + 3(3) = 14 ✓

Additionally, I verified using `numpy.linalg.solve`, which independently confirmed (1, 2, 3).

---

### Q7: What does the solution mean geometrically?

**A:** Each equation represents a plane in 3D space. The unique solution (1, 2, 3) is the single point where all three planes intersect.

---

### Q8: What would happen if two planes were parallel?

**A:** If two planes are parallel (and not coincident), the system has no solution — it is inconsistent. During elimination, we would encounter a row like [0 0 0 | c] where c ≠ 0, representing the contradiction 0 = c.

---

### Q9: When does a system have infinitely many solutions?

**A:** When the system is consistent but has at least one free variable — typically when one equation is a linear combination of the others. In the augmented matrix, this appears as a row of all zeros [0 0 0 | 0], and the system has fewer pivots than unknowns.

---

### Q10: What is a pivot?

**A:** A pivot is the first non-zero entry in a row of the matrix during elimination. Pivots are used to eliminate all entries below (and in RREF, above) them. In our final REF, the pivots are 1 (column 1), 1 (column 2), and 3 (column 3).

---

### Q11: Why did you choose Manim for this project?

**A:** Manim Community Edition is specifically designed for mathematical animations. It has built-in support for LaTeX typesetting, 3D scenes, and smooth transformations — ideal for visualising step-by-step algebraic procedures and geometric interpretations.

---

### Q12: Explain how the 3D scene demonstrates the effect of row operations.

**A:** In the 3D scene, each equation is a coloured plane. When we perform a row operation (e.g., R₂ ← R₂ − 2R₁), we replace the second equation with an equivalent one. The corresponding plane changes shape, but the intersection point (1, 2, 3) remains fixed. This visually confirms that row operations preserve the solution set.

---

### Q13: How did you ensure the narration was synchronised?

**A:** I followed an audio-first workflow:
1. Generated all narration audio using Edge TTS.
2. Measured actual durations with FFprobe.
3. Set animation `wait()` times to match audio durations.
4. Merged audio and video per scene using FFmpeg, using `tpad` to extend the last frame if the audio was longer than the animation.

---

### Q14: What are the limitations of Gaussian elimination?

**A:** 
- **Numerical instability:** Without partial pivoting, small pivot values can cause large rounding errors.
- **Complexity:** O(n³) for an n×n system, which is acceptable for small systems but costly for very large ones.
- **Not always applicable:** Requires the system to be expressible as an augmented matrix (must be linear).

---

### Q15: What would you improve if you had more time?

**A:**
- Add partial pivoting to handle cases where the natural pivot is zero or very small.
- Include an interactive UI where the viewer chooses which row operation to apply.
- Show RREF as well as REF to compare the two approaches.
- Add more special-case examples (parallel planes, infinite solutions) with full 3D visualisations.
