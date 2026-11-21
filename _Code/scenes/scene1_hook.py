"""
Scene 1 — Hook and Opening
Audio duration: 25.15s
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *


class Scene1_Hook(Scene):
    def construct(self):
        configure_scene(self)
        # Total target: ~25s

        # ── Cinematic title animation (0–5s) ──
        main_title = Text(
            "Gaussian Elimination",
            font_size=56, color=TITLE_COLOR, weight=BOLD,
        )
        sub_title = Text(
            "Solving a 3×3 System",
            font_size=40, color=ACCENT_COLOR,
        )
        sub_title.next_to(main_title, DOWN, buff=0.4)

        self.play(Write(main_title, run_time=1.5))
        self.play(FadeIn(sub_title, shift=UP * 0.3), run_time=0.8)
        # ~2.3s

        assessment = Text(
            "M3 Internal Assessment — Animation Video",
            font_size=26, color=SUBTITLE_COLOR,
        )
        assessment.next_to(sub_title, DOWN, buff=0.5)
        student_info = Text(
            "Gyanam  •  E25B070726",
            font_size=22, color=SUBTITLE_COLOR,
        )
        student_info.next_to(assessment, DOWN, buff=0.3)

        self.play(
            FadeIn(assessment, shift=UP * 0.2),
            FadeIn(student_info, shift=UP * 0.2),
            run_time=0.8,
        )
        self.wait(2.5)
        # ~5.6s — covers "Gaussian Elimination. Solving a 3x3 system..."

        # ── Clear title, show equations (~6–15s) ──
        self.play(
            FadeOut(main_title), FadeOut(sub_title),
            FadeOut(assessment), FadeOut(student_info),
            run_time=0.6,
        )

        eq1 = MathTex(r"x + y + z = 6", font_size=36, color=ROW1_COLOR)
        eq2 = MathTex(r"2x + 3y + z = 11", font_size=36, color=ROW2_COLOR)
        eq3 = MathTex(r"x + 2y + 3z = 14", font_size=36, color=ROW3_COLOR)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.4).move_to(LEFT * 3)

        self.play(
            LaggedStart(
                FadeIn(eq1, shift=RIGHT * 0.3),
                FadeIn(eq2, shift=RIGHT * 0.3),
                FadeIn(eq3, shift=RIGHT * 0.3),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(2.5)
        # ~10s — "Imagine three equations... substitution becomes messy"

        # ── Question marks (~15–18s) ──
        q_text = Text("Trial and error?\nSubstitution?", font_size=28, color="#ff6666", line_spacing=1.4)
        q_text.move_to(RIGHT * 3 + UP * 0.5)
        cross = Text("✗", font_size=48, color="#ff4444")
        cross.next_to(q_text, DOWN, buff=0.3)

        self.play(Write(q_text), run_time=0.8)
        self.play(FadeIn(cross, scale=1.5), run_time=0.4)
        self.wait(1.5)
        # ~13s

        # ── Gaussian elimination as solution (~18–25s) ──
        self.play(FadeOut(q_text), FadeOut(cross), run_time=0.4)

        sol_text = Text("Gaussian Elimination", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        sol_text.move_to(RIGHT * 3 + UP * 0.3)
        desc = Text(
            "A systematic algorithm\nthat always works.",
            font_size=24, color=WHITE, line_spacing=1.3,
        )
        desc.next_to(sol_text, DOWN, buff=0.3)

        arrow = Arrow(
            start=eqs.get_right() + RIGHT * 0.3,
            end=sol_text.get_left() + LEFT * 0.3,
            color=ACCENT_COLOR, buff=0.1,
        )

        self.play(GrowArrow(arrow), Write(sol_text), run_time=1.0)
        self.play(FadeIn(desc, shift=UP * 0.2), run_time=0.6)
        self.wait(5.0)
        # ~20s + enough buffer to reach ~25s

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.2)
