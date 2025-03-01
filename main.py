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
        with open(os.path.join(output_dir, text_file), "r") as f:
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
        "--voice", type=str, default=DEFAULT_VOICE, help="Voice to use for TTS"
    )
    parser.add_argument("--speed", type=float, default=1.0, help="Speed of the TTS")
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help="Sample rate of the audio",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    split_and_gen_audio(
        args.epub_path, args.output_dir, args.voice, args.speed, args.sample_rate
    )


if __name__ == "__main__":
    main()
