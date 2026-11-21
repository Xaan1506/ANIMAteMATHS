"""
Common configuration and helper utilities for all scenes.
"""
from manim import *
import numpy as np

# ─── Color palette ──────────────────────────────────────────────────
BG_COLOR = "#1a1a2e"
ROW1_COLOR = BLUE
ROW2_COLOR = GREEN
ROW3_COLOR = ORANGE
PIVOT_COLOR = YELLOW
CORRECT_COLOR = GREEN
OP_COLOR = WHITE
ACCENT_COLOR = "#00d4ff"  # Cyan
TITLE_COLOR = WHITE
SUBTITLE_COLOR = "#aaaacc"

# ─── Common config ──────────────────────────────────────────────────
FRAME_WIDTH = config.frame_width    # 14.22...
FRAME_HEIGHT = config.frame_height  # 8.0
SAFE_LEFT = -6.5
SAFE_RIGHT = 6.5
SAFE_TOP = 3.5
SAFE_BOTTOM = -3.5

# ─── Helper functions ───────────────────────────────────────────────

def configure_scene(scene):
    """Apply standard configuration to a scene."""
    scene.camera.background_color = BG_COLOR


def make_title(text, font_size=42, color=TITLE_COLOR):
    """Create a consistently styled title."""
    return Text(text, font_size=font_size, color=color, weight=BOLD)


def make_subtitle(text, font_size=28, color=SUBTITLE_COLOR):
    """Create a consistently styled subtitle."""
    return Text(text, font_size=font_size, color=color)


def make_body_text(text, font_size=24, color=WHITE, line_spacing=1.3):
    """Create readable body text, breaking long lines."""
    # Split long text into lines of ~55 chars
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 55:
            lines.append(" ".join(current_line))
            current_line = []
    if current_line:
        lines.append(" ".join(current_line))

    return Text(
        "\n".join(lines),
        font_size=font_size,
        color=color,
        line_spacing=line_spacing,
    )


def make_augmented_matrix(rows, row_colors=None, pivot_indices=None, font_size=36):
    """
    Create a colored augmented matrix.
    rows: list of [a, b, c, d] for [a b c | d]
    row_colors: list of colors for each row
    pivot_indices: list of (row, col) tuples to highlight as pivots
    """
    if row_colors is None:
        row_colors = [ROW1_COLOR, ROW2_COLOR, ROW3_COLOR]
    if pivot_indices is None:
        pivot_indices = []

    # Build LaTeX string
    entries = []
    for i, row in enumerate(rows):
        row_entries = []
        for j, val in enumerate(row):
            if isinstance(val, int) or (isinstance(val, float) and val == int(val)):
                val = int(val)
            # Format negative numbers properly
            s = str(val)
            if val < 0:
                s = str(val)
            row_entries.append(s)
        # Join with augmented bar before last column
        entries.append(row_entries)

    # Build the matrix using MathTex with array
    tex_rows = []
    for row_entries in entries:
        # First 3 entries, then bar, then last
        tex_row = " & ".join(row_entries[:3]) + " & " + row_entries[3]
        tex_rows.append(tex_row)

    tex_str = r"\left[\begin{array}{ccc|c} " + r" \\ ".join(tex_rows) + r" \end{array}\right]"
    matrix = MathTex(tex_str, font_size=font_size)

    # Color the rows
    # This is tricky with MathTex, so we'll just return the matrix for now
    # and color at a higher level if needed
    return matrix


def fade_all_out(scene, *mobjects, run_time=0.5):
    """Fade out all given mobjects."""
    anims = [FadeOut(m) for m in mobjects if m is not None]
    if anims:
        scene.play(*anims, run_time=run_time)


def safe_position(mobject, buff=0.3):
    """Ensure a mobject is within screen bounds."""
    if mobject.get_right()[0] > SAFE_RIGHT:
        mobject.shift(LEFT * (mobject.get_right()[0] - SAFE_RIGHT + buff))
    if mobject.get_left()[0] < SAFE_LEFT:
        mobject.shift(RIGHT * (SAFE_LEFT - mobject.get_left()[0] + buff))
    if mobject.get_top()[1] > SAFE_TOP:
        mobject.shift(DOWN * (mobject.get_top()[1] - SAFE_TOP + buff))
    if mobject.get_bottom()[1] < SAFE_BOTTOM:
        mobject.shift(UP * (SAFE_BOTTOM - mobject.get_bottom()[1] + buff))
    return mobject
