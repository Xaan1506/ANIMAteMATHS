"""
Scene 2 — Concept Introduction
Audio duration: 49.44s
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *


class Scene2_Concepts(Scene):
    def construct(self):
        configure_scene(self)
        # Total target: ~50s

        # ── Section title (~0–2s) ──
        section = make_title("Key Concepts", font_size=44)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)
        self.wait(0.5)

        # ── Ax = b (~2–12s) ──
        compact = MathTex(r"A\mathbf{x} = \mathbf{b}", font_size=48, color=WHITE)
        compact.next_to(section, DOWN, buff=0.6)

        a_label = Text("A = coefficient matrix", font_size=24, color=ROW1_COLOR)
        x_label = Text("x = unknowns vector", font_size=24, color=ACCENT_COLOR)
        b_label = Text("b = constants vector", font_size=24, color=ROW3_COLOR)

        labels = VGroup(a_label, x_label, b_label).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        labels.next_to(compact, DOWN, buff=0.4)

        self.play(Write(compact), run_time=0.8)
        self.play(
            LaggedStart(
                FadeIn(a_label, shift=RIGHT * 0.2),
                FadeIn(x_label, shift=RIGHT * 0.2),
                FadeIn(b_label, shift=RIGHT * 0.2),
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        self.wait(4.0)
        # ~8s

        # ── Augmented matrix (~12–18s) ──
        aug_label = Text("Augmented Matrix  [A | b]", font_size=28, color=ACCENT_COLOR, weight=BOLD)
        aug_label.next_to(labels, DOWN, buff=0.5)

        aug_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=34,
        )
        aug_mat.next_to(aug_label, DOWN, buff=0.3)

        self.play(Write(aug_label), run_time=0.5)
        self.play(FadeIn(aug_mat), run_time=0.8)
        self.wait(2.5)
        # ~12s

        # ── Clear and show row operations (~18–30s) ──
        self.play(
            FadeOut(compact), FadeOut(labels),
            FadeOut(aug_label), FadeOut(aug_mat),
            run_time=0.5,
        )

        ops_title = Text("Elementary Row Operations", font_size=30, color=ACCENT_COLOR, weight=BOLD)
        ops_title.next_to(section, DOWN, buff=0.5)

        op1 = Text("1. Swap two rows", font_size=24, color=WHITE)
        op2 = Text("2. Multiply a row by a non-zero scalar", font_size=24, color=WHITE)
        op3 = Text("3. Add a multiple of one row to another", font_size=24, color=WHITE)
        ops = VGroup(op1, op2, op3).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ops.next_to(ops_title, DOWN, buff=0.4)

        self.play(Write(ops_title), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(op1, shift=RIGHT * 0.2),
                FadeIn(op2, shift=RIGHT * 0.2),
                FadeIn(op3, shift=RIGHT * 0.2),
                lag_ratio=0.3,
            ),
            run_time=1.0,
        )
        self.wait(3.0)
        # ~17s

        # ── Pivot and REF (~30–38s) ──
        pivot_text = Text("Pivot: leading non-zero entry in each row", font_size=22, color=PIVOT_COLOR)
        ref_text = Text(
            "Row Echelon Form: staircase of pivots,\nall entries below each pivot are zero",
            font_size=22, color=WHITE, line_spacing=1.3,
        )
        pivot_ref = VGroup(pivot_text, ref_text).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        pivot_ref.next_to(ops, DOWN, buff=0.5)

        self.play(FadeIn(pivot_text, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(ref_text, shift=UP * 0.2), run_time=0.5)
        self.wait(5.0)
        # ~23s

        # ── Learning Objective (~38–50s) ──
        self.play(
            FadeOut(section), FadeOut(ops_title), FadeOut(ops),
            FadeOut(pivot_text), FadeOut(ref_text),
            run_time=0.5,
        )

        lo_title = Text("Learning Objective", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        lo_title.to_edge(UP, buff=0.8)

        lo_text = Text(
            "By the end of this video, the viewer will be able to explain\n"
            "how Gaussian elimination uses row operations to reduce a\n"
            "3×3 system to row echelon form, why those operations do not\n"
            "change the solution set, and what the solution means\n"
            "geometrically.",
            font_size=24, color=WHITE, line_spacing=1.5,
        )
        lo_text.next_to(lo_title, DOWN, buff=0.5)
        box = SurroundingRectangle(lo_text, color=ACCENT_COLOR, buff=0.3, corner_radius=0.1)

        self.play(Write(lo_title), run_time=0.5)
        self.play(FadeIn(lo_text), Create(box), run_time=1.0)
        self.wait(16.0)
        # ~41s+

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.2)
