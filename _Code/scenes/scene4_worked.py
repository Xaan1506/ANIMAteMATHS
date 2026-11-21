"""
Scene 4 — Complete Worked Example
Audio duration: 81.07s
Full augmented matrix construction, row operations with arithmetic,
pivots highlighted, back substitution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *


class Scene4_WorkedExample(Scene):
    def construct(self):
        configure_scene(self)

        # ── Show equations and matrix (~0–8s) ──
        title = make_title("Worked Example", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.5)

        eq1 = MathTex(r"x + y + z = 6", font_size=32, color=ROW1_COLOR)
        eq2 = MathTex(r"2x + 3y + z = 11", font_size=32, color=ROW2_COLOR)
        eq3 = MathTex(r"x + 2y + 3z = 14", font_size=32, color=ROW3_COLOR)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.3)
        eqs.next_to(title, DOWN, buff=0.4).shift(LEFT * 2.5)

        self.play(
            LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in eqs], lag_ratio=0.15),
            run_time=0.8,
        )
        self.wait(0.5)

        arrow = MathTex(r"\Rightarrow", font_size=36)
        arrow.next_to(eqs, RIGHT, buff=0.5)
        mat0 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=34,
        )
        mat0.next_to(arrow, RIGHT, buff=0.5)
        safe_position(mat0)

        self.play(Write(arrow), FadeIn(mat0), run_time=0.8)
        self.wait(2.5)

        # ── Center matrix for operations ──
        self.play(
            FadeOut(title), FadeOut(eqs), FadeOut(arrow),
            mat0.animate.move_to(UP * 2.1),
            run_time=0.6,
        )

        # ═══════════════════════════════════════════════
        # STEP 1: R2 → R2 − 2R1  (~6–20s)
        # ═══════════════════════════════════════════════
        step1_label = MathTex(r"R_2 \leftarrow R_2 - 2R_1", font_size=32, color=ACCENT_COLOR)
        step1_label.next_to(mat0, DOWN, buff=0.5)
        self.play(Write(step1_label), run_time=0.5)
        self.wait(0.5)

        arith1 = MathTex(
            r"[2 - 2(1),\; 3 - 2(1),\; 1 - 2(1) \;\mid\; 11 - 2(6)]",
            font_size=24, color=ROW2_COLOR,
        )
        arith1.next_to(step1_label, DOWN, buff=0.35)

        arith1_res = MathTex(
            r"=\quad [0,\; 1,\; -1 \;\mid\; -1]",
            font_size=26, color=ROW2_COLOR,
        )
        arith1_res.next_to(arith1, DOWN, buff=0.25)

        self.play(Write(arith1), run_time=1.0)
        self.wait(1.5)
        self.play(Write(arith1_res), run_time=0.6)
        self.wait(1.5)

        mat1 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=34,
        )
        mat1.move_to(UP * 2.1)

        self.play(FadeOut(arith1), FadeOut(arith1_res), Transform(mat0, mat1), run_time=0.8)
        self.wait(1.5)

        # ═══════════════════════════════════════════════
        # STEP 2: R3 → R3 − R1  (~20–35s)
        # ═══════════════════════════════════════════════
        self.play(FadeOut(step1_label), run_time=0.3)

        step2_label = MathTex(r"R_3 \leftarrow R_3 - R_1", font_size=32, color=ACCENT_COLOR)
        step2_label.next_to(mat0, DOWN, buff=0.5)
        self.play(Write(step2_label), run_time=0.5)
        self.wait(0.5)

        arith2 = MathTex(
            r"[1 - 1,\; 2 - 1,\; 3 - 1 \;\mid\; 14 - 6]",
            font_size=24, color=ROW3_COLOR,
        )
        arith2.next_to(step2_label, DOWN, buff=0.35)

        arith2_res = MathTex(
            r"=\quad [0,\; 1,\; 2 \;\mid\; 8]",
            font_size=26, color=ROW3_COLOR,
        )
        arith2_res.next_to(arith2, DOWN, buff=0.25)

        self.play(Write(arith2), run_time=1.0)
        self.wait(1.5)
        self.play(Write(arith2_res), run_time=0.6)
        self.wait(1.5)

        mat2 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 1 & 2 & 8 \end{array}\right]",
            font_size=34,
        )
        mat2.move_to(UP * 2.1)

        self.play(FadeOut(arith2), FadeOut(arith2_res), Transform(mat0, mat2), run_time=0.8)
        self.wait(1.5)

        # ═══════════════════════════════════════════════
        # STEP 3: R3 → R3 − R2  (~35–48s)
        # ═══════════════════════════════════════════════
        self.play(FadeOut(step2_label), run_time=0.3)

        step3_label = MathTex(r"R_3 \leftarrow R_3 - R_2", font_size=32, color=ACCENT_COLOR)
        step3_label.next_to(mat0, DOWN, buff=0.5)
        self.play(Write(step3_label), run_time=0.5)
        self.wait(0.5)

        arith3 = MathTex(
            r"[0 - 0,\; 1 - 1,\; 2 - (-1) \;\mid\; 8 - (-1)]",
            font_size=24, color=ROW3_COLOR,
        )
        arith3.next_to(step3_label, DOWN, buff=0.35)

        arith3_res = MathTex(
            r"=\quad [0,\; 0,\; 3 \;\mid\; 9]",
            font_size=26, color=ROW3_COLOR,
        )
        arith3_res.next_to(arith3, DOWN, buff=0.25)

        self.play(Write(arith3), run_time=1.0)
        self.wait(1.5)
        self.play(Write(arith3_res), run_time=0.6)
        self.wait(1.5)

        mat3 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 3 & 9 \end{array}\right]",
            font_size=34,
        )
        mat3.move_to(UP * 2.1)

        self.play(FadeOut(arith3), FadeOut(arith3_res), Transform(mat0, mat3), run_time=0.8)
        self.wait(0.5)

        # ═══════════════════════════════════════════════
        # ROW ECHELON FORM with pivot highlights (~48–55s)
        # ═══════════════════════════════════════════════
        self.play(FadeOut(step3_label), run_time=0.3)

        ref_label = Text("Row Echelon Form (REF)", font_size=30, color=PIVOT_COLOR, weight=BOLD)
        ref_label.next_to(mat0, DOWN, buff=0.45)

        pivot_note = Text(
            "Pivots: 1, 1, 3  (staircase pattern highlighted)",
            font_size=22, color=PIVOT_COLOR,
        )
        pivot_note.next_to(ref_label, DOWN, buff=0.3)

        rref_note = Text(
            "Note: In Reduced REF (RREF), pivots must equal 1\nand all entries above pivots must be zero.",
            font_size=20, color=SUBTITLE_COLOR, line_spacing=1.3,
        )
        rref_note.next_to(pivot_note, DOWN, buff=0.3)

        # Visible highlight boxes around pivots
        p1_box = Rectangle(width=0.45, height=0.45, color=YELLOW).move_to(mat0.get_center() + UP * 0.5 + LEFT * 1.0)
        p2_box = Rectangle(width=0.45, height=0.45, color=YELLOW).move_to(mat0.get_center() + LEFT * 0.45)
        p3_box = Rectangle(width=0.45, height=0.45, color=YELLOW).move_to(mat0.get_center() + DOWN * 0.5 + RIGHT * 0.1)
        pivot_boxes = VGroup(p1_box, p2_box, p3_box)

        self.play(Write(ref_label), Create(pivot_boxes), run_time=0.8)
        self.play(FadeIn(pivot_note), run_time=0.4)
        self.wait(2.0)
        self.play(FadeIn(rref_note), run_time=0.5)
        self.wait(3.5)

        # ═══════════════════════════════════════════════
        # BACK SUBSTITUTION (~55–81s)
        # ═══════════════════════════════════════════════
        self.play(
            FadeOut(ref_label), FadeOut(pivot_note), FadeOut(rref_note), FadeOut(pivot_boxes),
            run_time=0.4,
        )

        bs_title = Text("Back Substitution", font_size=32, color=ACCENT_COLOR, weight=BOLD)
        bs_title.next_to(mat0, DOWN, buff=0.4)
        self.play(Write(bs_title), run_time=0.5)

        # z
        bs_z1 = MathTex(r"3z = 9", font_size=30, color=ROW3_COLOR)
        bs_z2 = MathTex(r"\Rightarrow\quad z = 3", font_size=30, color=CORRECT_COLOR)
        bs_z = VGroup(bs_z1, bs_z2).arrange(RIGHT, buff=0.6)
        bs_z.next_to(bs_title, DOWN, buff=0.35)

        self.play(Write(bs_z1), run_time=0.5)
        self.wait(0.5)
        self.play(Write(bs_z2), run_time=0.4)
        self.wait(2.5)

        # y
        bs_y1 = MathTex(r"y - z = -1", font_size=30, color=ROW2_COLOR)
        bs_y2 = MathTex(r"y - 3 = -1", font_size=30)
        bs_y3 = MathTex(r"\Rightarrow\quad y = 2", font_size=30, color=CORRECT_COLOR)
        bs_y = VGroup(bs_y1, bs_y2, bs_y3).arrange(RIGHT, buff=0.4)
        bs_y.next_to(bs_z, DOWN, buff=0.3)

        self.play(Write(bs_y1), run_time=0.4)
        self.wait(0.3)
        self.play(Write(bs_y2), run_time=0.3)
        self.play(Write(bs_y3), run_time=0.3)
        self.wait(3.0)

        # x
        bs_x1 = MathTex(r"x + y + z = 6", font_size=30, color=ROW1_COLOR)
        bs_x2 = MathTex(r"x + 2 + 3 = 6", font_size=30)
        bs_x3 = MathTex(r"\Rightarrow\quad x = 1", font_size=30, color=CORRECT_COLOR)
        bs_x = VGroup(bs_x1, bs_x2, bs_x3).arrange(RIGHT, buff=0.4)
        bs_x.next_to(bs_y, DOWN, buff=0.3)

        self.play(Write(bs_x1), run_time=0.4)
        self.wait(0.3)
        self.play(Write(bs_x2), run_time=0.3)
        self.play(Write(bs_x3), run_time=0.3)
        self.wait(14.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.2)
