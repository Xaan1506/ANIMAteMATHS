"""
Scene 6 — Summary and Credits
Audio duration: 26.76s
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *


class Scene6_Summary(Scene):
    def construct(self):
        configure_scene(self)
        # Total target: ~27s

        # ── Takeaways (~0–10s) ──
        title = make_title("Key Takeaways", font_size=40)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.5)

        t1 = Text(
            "1. Gaussian elimination simplifies a system\n"
            "   using elementary row operations.",
            font_size=24, color=WHITE, line_spacing=1.3,
        )
        t2 = Text(
            "2. Row operations preserve the solution set.",
            font_size=24, color=WHITE,
        )
        t3 = Text(
            "3. Back substitution reveals the unknowns.",
            font_size=24, color=WHITE,
        )

        takeaways = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        takeaways.next_to(title, DOWN, buff=0.5).shift(LEFT * 1)

        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.8)
        self.wait(2.0)
        # ~6s

        # ── References and disclosure (~10–20s) ──
        self.play(FadeOut(title), FadeOut(takeaways), run_time=0.4)

        ref_title = Text("References & Disclosure", font_size=32, color=ACCENT_COLOR, weight=BOLD)
        ref_title.to_edge(UP, buff=0.5)

        refs = Text(
            "• Gilbert Strang — Introduction to Linear Algebra\n"
            "• David C. Lay — Linear Algebra and Its Applications\n"
            "• Manim Community Documentation",
            font_size=20, color=WHITE, line_spacing=1.5,
        )
        refs.next_to(ref_title, DOWN, buff=0.4)

        ai_text = Text(
            "Animation: Manim CE (Python)  •  Computation: NumPy\n"
            "Narration: Edge TTS (en-GB-RyanNeural)\n"
            "Coding assistance: Antigravity AI (Claude)",
            font_size=18, color=SUBTITLE_COLOR, line_spacing=1.4,
        )
        ai_text.next_to(refs, DOWN, buff=0.5)

        self.play(Write(ref_title), run_time=0.4)
        self.play(FadeIn(refs), run_time=0.5)
        self.wait(1.5)
        self.play(FadeIn(ai_text), run_time=0.5)
        self.wait(5.0)
        # ~15s

        # ── Thank you (~20–27s) ──
        self.play(FadeOut(ref_title), FadeOut(refs), FadeOut(ai_text), run_time=0.4)

        thanks = Text("Thank You", font_size=52, color=ACCENT_COLOR, weight=BOLD)
        student = Text("Gyanam  •  E25B070726", font_size=26, color=SUBTITLE_COLOR)
        student.next_to(thanks, DOWN, buff=0.4)

        self.play(FadeIn(thanks, scale=0.8), run_time=0.6)
        self.play(FadeIn(student, shift=UP * 0.2), run_time=0.4)
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
