"""
Scene 5 — Interpretation and Verification
Audio duration: 21.24s
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *


class Scene5_Verification(Scene):
    def construct(self):
        configure_scene(self)
        # Total target: ~21s

        # ── Solution display (~0–3s) ──
        title = make_title("Verification", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.4)

        solution = MathTex(r"(x, y, z) = (1, 2, 3)", font_size=42, color=CORRECT_COLOR)
        solution.next_to(title, DOWN, buff=0.5)
        sol_box = SurroundingRectangle(solution, color=CORRECT_COLOR, buff=0.2, corner_radius=0.1)

        self.play(Write(solution), Create(sol_box), run_time=0.6)
        self.wait(0.5)
        # ~1.5s

        # ── Substitution checks (~3–10s) ──
        v1 = MathTex(r"1 + 2 + 3 = 6", font_size=28, color=ROW1_COLOR)
        check1 = Text("✓", font_size=32, color=CORRECT_COLOR)

        v2 = MathTex(r"2(1) + 3(2) + 3 = 11", font_size=28, color=ROW2_COLOR)
        check2 = Text("✓", font_size=32, color=CORRECT_COLOR)

        v3 = MathTex(r"1 + 2(2) + 3(3) = 14", font_size=28, color=ROW3_COLOR)
        check3 = Text("✓", font_size=32, color=CORRECT_COLOR)

        checks = VGroup(
            VGroup(v1, check1).arrange(RIGHT, buff=0.4),
            VGroup(v2, check2).arrange(RIGHT, buff=0.4),
            VGroup(v3, check3).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.25)
        checks.next_to(sol_box, DOWN, buff=0.4)
        safe_position(checks)

        for eq_group in checks:
            eq, chk = eq_group[0], eq_group[1]
            chk.set_opacity(0)
            self.play(Write(eq), run_time=0.4)
            self.play(chk.animate.set_opacity(1), run_time=0.3)
            self.wait(0.3)
        self.wait(0.5)
        # ~5s

        # ── Special cases (~10–21s) ──
        self.play(
            FadeOut(title), FadeOut(solution), FadeOut(sol_box), FadeOut(checks),
            run_time=0.4,
        )

        special_title = Text("Special Cases", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        special_title.to_edge(UP, buff=0.5)
        self.play(Write(special_title), run_time=0.4)

        # Special cases groups
        incon_label = Text("No Solution:", font_size=24, color="#ff6666", weight=BOLD)
        incon_row = MathTex(
            r"\left[\begin{array}{ccc|c} 0 & 0 & 0 & 5 \end{array}\right]",
            font_size=28,
        )
        incon_expl = Text("→  0 = 5  (Inconsistent / Contradiction)", font_size=20, color="#ff6666")
        case1 = VGroup(incon_label, incon_row, incon_expl).arrange(RIGHT, buff=0.4)

        dep_label = Text("Infinitely Many:", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        dep_row = MathTex(
            r"\left[\begin{array}{ccc|c} 0 & 0 & 0 & 0 \end{array}\right]",
            font_size=28,
        )
        dep_expl = Text("→  Dependent equation (Free variables)", font_size=20, color=WHITE)
        case2 = VGroup(dep_label, dep_row, dep_expl).arrange(RIGHT, buff=0.4)

        cases = VGroup(case1, case2).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        cases.next_to(special_title, DOWN, buff=0.8)
        safe_position(cases)

        self.play(FadeIn(case1, shift=UP * 0.2), run_time=0.8)
        self.wait(3.5)
        self.play(FadeIn(case2, shift=UP * 0.2), run_time=0.8)
        self.wait(6.0)
        # ~16s+

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.wait(0.2)
