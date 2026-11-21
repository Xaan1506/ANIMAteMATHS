#!/usr/bin/env python3
"""
Generate TTS audio for each scene using Edge TTS (en-GB-RyanNeural).
Falls back to gTTS if Edge TTS fails.
Outputs per-scene MP3 files and a timing manifest.
"""
import asyncio
import json
import os
import sys
import subprocess

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from narration_script import NARRATION

VOICE = "en-GB-RyanNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "timing_manifest.json")


def get_audio_duration(filepath):
    """Get audio duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


async def generate_edge_tts(text, output_path):
    """Generate audio using Edge TTS."""
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE, rate="-5%")
    await communicate.save(output_path)


def generate_gtts(text, output_path):
    """Fallback: generate audio using gTTS."""
    from gtts import gTTS
    tts = gTTS(text=text, lang='en', tld='co.uk')
    tts.save(output_path)


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    manifest = {}

    for scene_key in sorted(NARRATION.keys()):
        full_text = " ".join(NARRATION[scene_key])
        output_path = os.path.join(OUTPUT_DIR, f"{scene_key}.mp3")
        print(f"\nGenerating audio for {scene_key}...")
        print(f"  Text ({len(full_text.split())} words): {full_text[:80]}...")

        # Try Edge TTS first
        try:
            await generate_edge_tts(full_text, output_path)
            tts_engine = "edge-tts"
            print(f"  ✓ Edge TTS succeeded")
        except Exception as e:
            print(f"  ✗ Edge TTS failed: {e}")
            print(f"  Falling back to gTTS...")
            try:
                generate_gtts(full_text, output_path)
                tts_engine = "gtts"
                print(f"  ✓ gTTS succeeded")
            except Exception as e2:
                print(f"  ✗ gTTS also failed: {e2}")
                manifest[scene_key] = {"error": str(e2)}
                continue

        # Measure duration
        duration = get_audio_duration(output_path)
        file_size = os.path.getsize(output_path)
        print(f"  Duration: {duration:.2f}s, Size: {file_size} bytes")
        print(f"  Engine: {tts_engine}")

        manifest[scene_key] = {
            "file": output_path,
            "duration": round(duration, 2),
            "size": file_size,
            "engine": tts_engine,
            "word_count": len(full_text.split()),
        }

    # Save manifest
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"\n✓ Timing manifest saved to {MANIFEST_PATH}")

    # Print summary
    total = sum(v.get("duration", 0) for v in manifest.values())
    print(f"\nTotal audio duration: {total:.2f}s ({total/60:.1f} min)")
    for k, v in sorted(manifest.items()):
        if "duration" in v:
            print(f"  {k}: {v['duration']:.2f}s")

    return manifest


if __name__ == "__main__":
    asyncio.run(main())
