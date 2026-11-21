"""
Scene 3 — Visual Intuition (3D)
Audio duration: 33.55s
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manim import *
from helpers.common import *
import numpy as np


class Scene3_3DIntuition(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        # Total target: ~34s

        # ── Title ──
        title = Text("Visual Intuition: Three Planes", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)

        # ── 3D axes ──
        axes = ThreeDAxes(
            x_range=[-1, 5, 1], y_range=[-1, 5, 1], z_range=[-1, 5, 1],
            x_length=5, y_length=5, z_length=5,
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), run_time=0.8)
        # ~1.5s

        # ── Planes ──
        plane1 = Surface(
            lambda u, v: axes.c2p(u, v, 6 - u - v),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(10, 10), fill_opacity=0.3, stroke_width=0.5,
        ).set_color(BLUE)

        plane2 = Surface(
            lambda u, v: axes.c2p(u, v, 11 - 2*u - 3*v),
            u_range=[0, 4], v_range=[0, 3],
            resolution=(10, 10), fill_opacity=0.3, stroke_width=0.5,
        ).set_color(GREEN)

        plane3 = Surface(
            lambda u, v: axes.c2p(u, v, (14 - u - 2*v)/3),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(10, 10), fill_opacity=0.3, stroke_width=0.5,
        ).set_color(ORANGE)

        # Equation labels
        eq1_label = MathTex(r"x + y + z = 6", font_size=24, color=BLUE)
        eq2_label = MathTex(r"2x + 3y + z = 11", font_size=24, color=GREEN)
        eq3_label = MathTex(r"x + 2y + 3z = 14", font_size=24, color=ORANGE)
        eq_group = VGroup(eq1_label, eq2_label, eq3_label).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        eq_group.to_corner(DL, buff=0.5)
        self.add_fixed_in_frame_mobjects(eq_group)

        # Animate planes one at a time (~2–12s)
        self.play(Create(plane1), FadeIn(eq1_label), run_time=1.2)
        self.wait(1.5)
        self.play(Create(plane2), FadeIn(eq2_label), run_time=1.2)
        self.wait(1.5)
        self.play(Create(plane3), FadeIn(eq3_label), run_time=1.2)
        self.wait(1.5)
        # ~10s

        # ── Intersection point (~12–18s) ──
        point = Dot3D(axes.c2p(1, 2, 3), color=YELLOW, radius=0.12)
        point_label = MathTex(r"(1, 2, 3)", font_size=28, color=YELLOW)
        point_label.to_corner(DR, buff=0.8)
        self.add_fixed_in_frame_mobjects(point_label)

        self.play(
            Create(point),
            FadeIn(point_label),
            Flash(point, color=YELLOW, flash_radius=0.3),
            run_time=0.8,
        )
        self.wait(2.0)
        # ~13s

        # ── Camera rotation (~18–28s) ──
        self.begin_ambient_camera_rotation(rate=0.15)

        expl = Text(
            "Row operations change the planes\nbut preserve the intersection point.",
            font_size=20, color=WHITE, line_spacing=1.3,
        )
        expl.next_to(title, DOWN, buff=0.4).to_edge(RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(expl)
        self.play(FadeIn(expl, shift=LEFT * 0.3), run_time=0.6)
        self.wait(4.0)
        # ~18s

        # Demonstrate plane change
        plane2_new = Surface(
            lambda u, v: axes.c2p(u, v, v + 1),
            u_range=[0, 4], v_range=[0, 3.5],
            resolution=(10, 10), fill_opacity=0.3, stroke_width=0.5,
        ).set_color(GREEN_B)

        self.play(Transform(plane2, plane2_new), run_time=1.2)
        self.play(Flash(point, color=YELLOW, flash_radius=0.4), run_time=0.6)
        self.wait(5.0)
        # ~25s

        self.stop_ambient_camera_rotation()
        self.wait(3.0)
        # ~28s

        # ── Fade out ──
        self.play(
            *[FadeOut(m) for m in [axes, plane1, plane2, plane3, point, title]],
            run_time=0.5,
        )
        self.remove_fixed_in_frame_mobjects(eq_group, point_label, expl, title)
        self.play(FadeOut(eq_group), FadeOut(point_label), FadeOut(expl), run_time=0.4)
        self.wait(0.2)
