# Gaussian Elimination — M3 Internal Assessment Animation Video

## Student Details

| Field | Detail |
|---|---|
| **Name** | Gyanam |
| **Student ID** | E25B070726 |
| **Subject** | Mathematics 3 — Linear Algebra and Calculus |
| **Batch** | Hopper |
| **Topic** | Gaussian Elimination: Solving a 3×3 System of Linear Equations |

## Learning Objective

By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3×3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically.

## Project Overview

This project produces a 5-minute animated video explaining Gaussian elimination through six scenes:

1. **Hook and Opening** — Introduces the problem and motivates the method.
2. **Concept Introduction** — Defines key notation: system of equations, Ax = b, augmented matrix, row operations, pivot, REF.
3. **Visual Intuition** — 3D animation of three planes intersecting at the solution point (1, 2, 3).
4. **Worked Example** — Step-by-step row reduction with arithmetic and back substitution.
5. **Verification** — Substitution check and discussion of special cases (no solution, infinite solutions).
6. **Summary and Credits** — Key takeaways, references, and disclosures.

## System Solved

```
x + y + z = 6
2x + 3y + z = 11
x + 2y + 3z = 14
```

**Solution: (x, y, z) = (1, 2, 3)**

Verified by NumPy (`numpy.linalg.solve`) and manual back substitution.

## Tools Used

| Tool | Purpose |
|---|---|
| **Python 3** | Programming language |
| **Manim Community Edition** | Mathematical animation engine |
| **NumPy** | Mathematical verification |
| **Edge TTS** | Text-to-speech narration (en-GB-RyanNeural) |
| **FFmpeg** | Audio/video merging and encoding |
| **LaTeX** | Mathematical typesetting |

## How to Reproduce

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r _Code/requirements.txt

# 3. Verify mathematics
python _Code/helpers/verify_math.py

# 4. Generate narration audio
python _Code/scripts/generate_audio.py

# 5. Render all scenes and produce final video
python _Code/scripts/render_all.py
```

### Prerequisites

- Python 3.10+
- FFmpeg (with libx264 and AAC support)
- LaTeX distribution (BasicTeX or TeX Live)
- Internet connection (for Edge TTS)

## Project Structure

```
ANIMATION/
├── _Video.mp4                  # Final narrated video
├── README.md                   # This file
├── Storyboard.md               # Scene-by-scene storyboard
├── Narration_Script.md         # Complete narration by scene
├── Code_Walkthrough.md         # Explanation of every code file
├── Viva_Prep.md                # 15 viva questions and answers
├── _Code/
│   ├── requirements.txt
│   ├── narration_script.py     # Narration text data
│   ├── scenes/
│   │   ├── scene1_hook.py      # Scene 1 — Hook
│   │   ├── scene2_concepts.py  # Scene 2 — Concepts
│   │   ├── scene3_3d.py        # Scene 3 — 3D Intuition
│   │   ├── scene4_worked.py    # Scene 4 — Worked Example
│   │   ├── scene5_verify.py    # Scene 5 — Verification
│   │   └── scene6_summary.py   # Scene 6 — Summary
│   ├── helpers/
│   │   ├── common.py           # Shared styles and utilities
│   │   └── verify_math.py      # NumPy verification
│   ├── scripts/
│   │   ├── generate_audio.py   # TTS audio generation
│   │   └── render_all.py       # Master render and merge script
│   └── audio/                  # Generated MP3 files
└── media/                      # Manim rendering output
```

## References

1. Gilbert Strang — *Introduction to Linear Algebra*, 5th Edition.
2. David C. Lay — *Linear Algebra and Its Applications*, 6th Edition.
3. Manim Community Documentation — https://docs.manim.community/

## AI Disclosure

| AI Tool | Use |
|---|---|
| **Antigravity AI (Claude)** | Coding assistance, project structuring, script writing |
| **Edge TTS (en-GB-RyanNeural)** | Voice narration generation |

The mathematical content, storyboard design, and learning objectives were created by the student. AI tools were used as assistants for code development and voice synthesis.

## License

This project was created for academic assessment purposes at PES University.
