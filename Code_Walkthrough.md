# Code Walkthrough — Gaussian Elimination Animation

**Student:** Gyanam (E25B070726)

This document explains the purpose and structure of every code file in the project.

---

## Project Architecture

The code is organised into three main folders:

```
_Code/
├── narration_script.py      # Central narration data
├── scenes/                  # One Manim scene file per video section
├── helpers/                 # Shared utilities and verification
├── scripts/                 # Build scripts (audio generation, rendering)
└── audio/                   # Generated MP3 files and timing manifest
```

---

## 1. `narration_script.py`

**Purpose:** Stores all narration text as a Python dictionary, keyed by scene name.

- Each scene maps to a list of narration segments (sentences or phrases).
- `get_full_narration(scene_key)` joins all segments into one string for TTS.
- `get_segments(scene_key)` returns individual segments for timing purposes.

This file is the single source of truth for all spoken content. The TTS generation script imports from here.

---

## 2. `helpers/common.py`

**Purpose:** Defines shared constants and helper functions used across all scenes.

**Key contents:**
- **Color palette:** `BG_COLOR` (dark navy), row colours (Blue, Green, Orange), `PIVOT_COLOR` (Yellow), `ACCENT_COLOR` (Cyan).
- **Safe zone constants:** `SAFE_LEFT`, `SAFE_RIGHT`, `SAFE_TOP`, `SAFE_BOTTOM` — boundaries to prevent off-screen content.
- **`configure_scene(scene)`** — Sets the standard background colour.
- **`make_title()`, `make_subtitle()`, `make_body_text()`** — Consistent text styling with auto line-breaking.
- **`make_augmented_matrix()`** — Builds a coloured augmented matrix using LaTeX `array` environment.
- **`safe_position()`** — Shifts any mobject back on-screen if it overflows.
- **`fade_all_out()`** — Convenience function to fade out multiple mobjects.

---

## 3. `helpers/verify_math.py`

**Purpose:** Independent NumPy verification of every mathematical step.

**What it checks:**
1. Original augmented matrix is correct.
2. R₂ ← R₂ − 2R₁ produces [0, 1, −1, −1].
3. R₃ ← R₃ − R₁ produces [0, 1, 2, 8].
4. R₃ ← R₃ − R₂ produces [0, 0, 3, 9].
5. Back substitution gives z = 3, y = 2, x = 1.
6. Substitution into all three original equations.
7. Cross-check with `numpy.linalg.solve`.

If any assertion fails, the script terminates with an error.

---

## 4. Scene Files (`scenes/`)

### `scene1_hook.py` — Scene1_Hook

**Duration:** ~25 seconds  
**Type:** Standard 2D `Scene`

Creates the cinematic opening:
1. Animated title "Gaussian Elimination: Solving a 3×3 System".
2. Assessment subtitle and student info.
3. Three colour-coded equations.
4. "Trial and error?" crossed out.
5. Arrow pointing to "Gaussian Elimination" as the systematic method.

### `scene2_concepts.py` — Scene2_Concepts

**Duration:** ~50 seconds  
**Type:** Standard 2D `Scene`

Defines all mathematical notation:
1. General system of linear equations.
2. Compact form Ax = b with labelled components.
3. Augmented matrix example using the actual problem.
4. Three elementary row operations listed.
5. Pivot and row echelon form defined.
6. Learning objective in a highlighted box.

### `scene3_3d.py` — Scene3_3DIntuition

**Duration:** ~35 seconds  
**Type:** `ThreeDScene` (3D camera)

Creates the geometric visualisation:
1. 3D axes set up.
2. Three translucent coloured planes (one per equation).
3. Planes appear sequentially with equation labels.
4. Yellow dot at intersection point (1, 2, 3).
5. Ambient camera rotation for depth.
6. One plane transforms (simulating a row operation) while the intersection point stays fixed.

### `scene4_worked.py` — Scene4_WorkedExample

**Duration:** ~90 seconds  
**Type:** Standard 2D `Scene`

The core mathematical content:
1. Equations → augmented matrix transformation.
2. Three row operations, each with:
   - Operation notation (e.g., R₂ ← R₂ − 2R₁).
   - Entry-by-entry arithmetic.
   - Resulting matrix via `Transform`.
3. Row echelon form displayed with pivot note.
4. REF vs RREF distinction.
5. Back substitution: z → y → x, each with intermediate steps.

### `scene5_verify.py` — Scene5_Verification

**Duration:** ~40 seconds  
**Type:** Standard 2D `Scene`

1. Solution displayed in a green box.
2. Three substitution verifications with animated ✓.
3. Special cases:
   - [0 0 0 | 5] → inconsistent (no solution).
   - [0 0 0 | 0] → dependent equation (possibly infinite solutions).

### `scene6_summary.py` — Scene6_Summary

**Duration:** ~25 seconds  
**Type:** Standard 2D `Scene`

1. Three takeaways with sequential fade-in.
2. References list.
3. AI tools disclosure.
4. "Thank You" closing.

---

## 5. `scripts/generate_audio.py`

**Purpose:** Generates MP3 narration files for each scene.

**Process:**
1. Imports `NARRATION` from `narration_script.py`.
2. For each scene, joins all segments into one string.
3. Calls Edge TTS (en-GB-RyanNeural, rate −5%) to generate MP3.
4. Falls back to gTTS if Edge TTS fails.
5. Measures actual duration using `ffprobe`.
6. Writes `timing_manifest.json` with durations and file paths.

---

## 6. `scripts/render_all.py`

**Purpose:** Master build script that renders all scenes and produces the final video.

**Process:**
1. Loads the audio timing manifest.
2. Renders each scene using `manim render -qh`.
3. Merges each scene's video with its corresponding MP3 audio using FFmpeg.
   - If audio is longer than video, extends the last frame using `tpad`.
4. Concatenates all merged scene videos into one final MP4.
5. Runs `ffprobe` verification on the final video.

**FFmpeg settings:** H.264, CRF 20, AAC 192k, 30 FPS, `faststart`.

---

## Design Decisions

1. **Separate scene files** rather than one monolithic file — easier to debug, re-render individual scenes, and maintain.
2. **Audio-first workflow** — narration is generated first, durations measured, then animation timing is built to match.
3. **NumPy verification** runs independently of Manim — mathematics is correct regardless of rendering issues.
4. **Safe positioning** — all text and equations are checked against screen boundaries before display.
5. **Colour consistency** — defined once in `common.py` and imported everywhere.
