#!/usr/bin/env python3
"""
Master render script: renders each scene, merges with audio, and produces final video.
Usage: python render_all.py [--quality low|medium|high]
"""
import json
import os
import subprocess
import sys
import shutil

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE_DIR = os.path.join(PROJECT_DIR, "_Code")
AUDIO_DIR = os.path.join(CODE_DIR, "audio")
SCENES_DIR = os.path.join(CODE_DIR, "scenes")
MEDIA_DIR = os.path.join(PROJECT_DIR, "media")
OUTPUT_DIR = os.path.join(MEDIA_DIR, "scenes")
MANIFEST_PATH = os.path.join(AUDIO_DIR, "timing_manifest.json")
FINAL_VIDEO = os.path.join(PROJECT_DIR, "_Video.mp4")

# Scene definitions: (file, class_name, scene_key)
SCENES = [
    ("scene1_hook.py", "Scene1_Hook", "scene1"),
    ("scene2_concepts.py", "Scene2_Concepts", "scene2"),
    ("scene3_3d.py", "Scene3_3DIntuition", "scene3"),
    ("scene4_worked.py", "Scene4_WorkedExample", "scene4"),
    ("scene5_verify.py", "Scene5_Verification", "scene5"),
    ("scene6_summary.py", "Scene6_Summary", "scene6"),
]


def get_quality_flag(quality="high"):
    """Return manim quality flags for 1080p 30fps."""
    if quality == "high":
        return ["--resolution", "1920,1080", "--fps", "30"]
    elif quality == "medium":
        return ["--resolution", "1280,720", "--fps", "30"]
    else:
        return ["--resolution", "854,480", "--fps", "15"]


def render_scene(scene_file, class_name, quality="high"):
    """Render a single Manim scene."""
    scene_path = os.path.join(SCENES_DIR, scene_file)
    qflags = get_quality_flag(quality)

    print(f"\n{'='*60}")
    print(f"Rendering {class_name} from {scene_file}...")
    print(f"{'='*60}")

    cmd = [
        sys.executable, "-m", "manim",
        "render",
    ] + qflags + [
        scene_path, class_name,
        "--media_dir", MEDIA_DIR,
    ]
    print(f"  Command: {' '.join(cmd)}")

    env = os.environ.copy()
    tex_bin = "/tmp/basictex/usr/local/texlive/2026basic/bin/universal-darwin"
    if tex_bin not in env.get("PATH", ""):
        env["PATH"] = f"{tex_bin}:{env.get('PATH', '')}"

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR, env=env)
    if result.returncode != 0:
        print(f"  ✗ FAILED:\n{result.stderr}")
        return None

    # Find the rendered file by looking for the latest file matching class_name
    candidates = []
    for root, dirs, files in os.walk(os.path.join(MEDIA_DIR, "videos")):
        for f in files:
            if f.endswith(".mp4") and class_name in f and "partial" not in root:
                full_p = os.path.join(root, f)
                candidates.append((os.path.getmtime(full_p), full_p))

    if not candidates:
        print(f"  ✗ Could not find rendered video for {class_name}")
        return None

    candidates.sort(reverse=True)
    output_path = candidates[0][1]
    print(f"  ✓ Rendered: {output_path}")
    return output_path


def merge_audio_video(video_path, audio_path, output_path):
    """Merge audio and video using FFmpeg, cleanly synchronising stream lengths."""
    print(f"\n  Merging audio + video -> {output_path}")

    vid_dur = get_duration(video_path)
    aud_dur = get_duration(audio_path)
    print(f"    Video duration: {vid_dur:.2f}s")
    print(f"    Audio duration: {aud_dur:.2f}s")

    if aud_dur > vid_dur:
        pad_v = aud_dur - vid_dur + 0.3
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", f"[0:v]tpad=stop_mode=clone:stop_duration={pad_v}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-r", "30",
            "-shortest",
            output_path,
        ]
    else:
        pad_a = vid_dur - aud_dur + 0.3
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", f"[1:a]apad=pad_dur={pad_a}[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-r", "30",
            "-shortest",
            output_path,
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ✗ FFmpeg merge failed:\n{result.stderr}")
        return False
    print(f"    ✓ Merged successfully")
    return True


def get_duration(filepath):
    """Get media file duration in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def concatenate_scenes(scene_files, output_path):
    """Concatenate all scene videos into final video."""
    print(f"\n{'='*60}")
    print("Concatenating all scenes into final video...")
    print(f"{'='*60}")

    # Create concat file
    concat_file = os.path.join(MEDIA_DIR, "concat_list.txt")
    with open(concat_file, 'w') as f:
        for sf in scene_files:
            f.write(f"file '{sf}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-r", "30",
        "-movflags", "+faststart",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ Concatenation failed:\n{result.stderr}")
        return False

    print(f"  ✓ Final video: {output_path}")
    return True


def verify_final(video_path):
    """Run ffprobe on final video to verify specs."""
    print(f"\n{'='*60}")
    print("Final video verification")
    print(f"{'='*60}")

    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)

    # Check video stream
    video_stream = None
    audio_stream = None
    for s in info.get("streams", []):
        if s["codec_type"] == "video":
            video_stream = s
        elif s["codec_type"] == "audio":
            audio_stream = s

    duration = float(info["format"]["duration"])
    print(f"  Duration: {duration:.2f}s ({duration/60:.1f} min)")
    print(f"  File size: {int(info['format']['size'])/1024/1024:.1f} MB")

    if video_stream:
        print(f"  Video codec: {video_stream['codec_name']}")
        print(f"  Resolution: {video_stream['width']}x{video_stream['height']}")
        fps = eval(video_stream.get('r_frame_rate', '30/1'))
        print(f"  FPS: {fps}")
    else:
        print("  ✗ NO VIDEO STREAM!")

    if audio_stream:
        print(f"  Audio codec: {audio_stream['codec_name']}")
        print(f"  Audio channels: {audio_stream.get('channels', '?')}")
    else:
        print("  ✗ NO AUDIO STREAM!")

    if duration > 420:
        print(f"  ⚠ Duration exceeds 7 minutes!")
    elif duration < 240:
        print(f"  ⚠ Duration is under 4 minutes - may be too short")

    return {
        "duration": duration,
        "has_video": video_stream is not None,
        "has_audio": audio_stream is not None,
        "resolution": f"{video_stream['width']}x{video_stream['height']}" if video_stream else None,
        "video_codec": video_stream['codec_name'] if video_stream else None,
        "audio_codec": audio_stream['codec_name'] if audio_stream else None,
    }


def main():
    quality = "high"
    if len(sys.argv) > 2 and sys.argv[1] == "--quality":
        quality = sys.argv[2]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load audio manifest
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    print("Audio manifest loaded:")
    for k, v in sorted(manifest.items()):
        print(f"  {k}: {v.get('duration', 'N/A')}s")

    # Render and merge each scene
    merged_files = []
    for scene_file, class_name, scene_key in SCENES:
        # Render
        video_path = render_scene(scene_file, class_name, quality)
        if video_path is None:
            print(f"\n✗ FAILED to render {scene_file}. Stopping.")
            sys.exit(1)

        # Merge with audio
        audio_path = manifest[scene_key]["file"]
        merged_path = os.path.join(OUTPUT_DIR, f"{scene_key}_merged.mp4")
        success = merge_audio_video(video_path, audio_path, merged_path)
        if not success:
            print(f"\n✗ FAILED to merge {scene_key}. Stopping.")
            sys.exit(1)

        merged_files.append(merged_path)

    # Concatenate all scenes
    success = concatenate_scenes(merged_files, FINAL_VIDEO)
    if not success:
        print("\n✗ FAILED to concatenate scenes.")
        sys.exit(1)

    # Verify
    result = verify_final(FINAL_VIDEO)
    if result["has_video"] and result["has_audio"]:
        print(f"\n{'='*60}")
        print("✓ FINAL VIDEO READY!")
        print(f"  File: {FINAL_VIDEO}")
        print(f"  Duration: {result['duration']:.1f}s")
        print(f"{'='*60}")
    else:
        print("\n✗ Final video has missing streams!")
        sys.exit(1)


if __name__ == "__main__":
    main()
