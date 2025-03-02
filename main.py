import argparse
import os
import re

from chapterizer import Chapterizer
from defaults import *
from tts import gen_audio


def split_and_gen_audio(
    epub_path,
    output_dir,
    voice=DEFAULT_VOICE,
    speed=DEFAULT_SPEED,
    sample_rate=DEFAULT_SAMPLE_RATE,
):
    chapterizer = Chapterizer(epub_path, output_dir)
    generated_text_files = chapterizer.chapterize()

    for text_file in generated_text_files:
        text = ""
        with open(os.path.join(output_dir, text_file), "r", encoding="utf-8") as f:
            text = f.read()
        audio_file = re.sub(r"\.txt$", ".mp3", text_file)
        gen_audio(text, os.path.join(output_dir, audio_file), voice, speed, sample_rate)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate audio from EPUB file")
    parser.add_argument("epub_path", type=str, help="Path to the EPUB file")
    parser.add_argument(
        "output_dir", type=str, help="Directory to save the output audio files"
    )
    parser.add_argument(
        "--voice", type=str, default=DEFAULT_VOICE, help=f"Voice to use for TTS (default: {DEFAULT_VOICE})"
    )
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED, help=f"Speed of the TTS (default: {DEFAULT_SPEED})")
    return parser.parse_args()


def main():
    args = parse_args()
    split_and_gen_audio(
        args.epub_path, args.output_dir, args.voice, args.speed
    )


if __name__ == "__main__":
    main()
