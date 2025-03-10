import argparse
import importlib

import numpy as np
import soundfile as sf
from rich import print

from audiobook_generator.util import is_mps_fallback_enabled, is_mps_supported

from .defaults import *


def gen_audio(
    text,
    audio_file,
    voice=DEFAULT_VOICE,
    speed=DEFAULT_SPEED,
    format=DEFAULT_FORMAT,
):
    # 'a' => American English, ' => British English
    # 'j' => Japanese: pip install misaki[ja]
    # 'z => Mandarin Chinese: pip install misaki[zh]
    lang_code = voice[0]
    device = None
    if is_mps_supported() and is_mps_fallback_enabled():
        print("[italic]Using MPS device with fallback.[/italic]")
        device = "mps"
    kokoro = importlib.import_module("kokoro")
    pipeline = kokoro.KPipeline(
        lang_code=lang_code, repo_id="hexgrad/Kokoro-82M", device=device
    )  # <= make sure lang_code matches voice
    # pipeline = KPipeline(
    #     lang_code=lang_code, repo_id="hexgrad/Kokoro-82M-v1.1-zh"
    # )  # <= make sure lang_code matches voice
    generator = pipeline(text, voice, speed)
    audios = []
    for _, _, audio in generator:
        audios.append(audio)
    audios = np.concatenate(audios)
    sf.write(audio_file, audios, DEFAULT_SAMPLE_RATE, format=format)


def main():

    parser = argparse.ArgumentParser(description="Convert text to speech")
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("audio_file", help="Output audio filename")
    parser.add_argument(
        "--voice",
        default=DEFAULT_VOICE,
        help=f"Voice to use (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help=f"Speech speed (default: {DEFAULT_SPEED})",
    )
    parser.add_argument(
        "--f",
        "--format",
        type=str,
        default=DEFAULT_FORMAT,
        help=f"Audio format (default: {DEFAULT_FORMAT})",
    )

    args = parser.parse_args()

    gen_audio(
        args.text,
        args.audio_file,
        voice=args.voice,
        speed=args.speed,
        format=args.format,
    )
    print(f"Audio saved to {args.audio_file}")


if __name__ == "__main__":
    main()
