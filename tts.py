import argparse

import numpy as np
import soundfile as sf
from kokoro import KPipeline

from defaults import *


def gen_audio(
    text,
    audio_file,
    voice=DEFAULT_VOICE,
    speed=DEFAULT_SPEED,
    sample_rate=DEFAULT_SAMPLE_RATE,
):
    # 'a' => American English, ' => British English
    # 'j' => Japanese: pip install misaki[ja]
    # 'z' => Mandarin Chinese: pip install misaki[zh]
    lang_code = voice[0]
    pipeline = KPipeline(
        lang_code=lang_code, repo_id="hexgrad/Kokoro-82M"
    )  # <= make sure lang_code matches voice
    # pipeline = KPipeline(
    #     lang_code=lang_code, repo_id="hexgrad/Kokoro-82M-v1.1-zh"
    # )  # <= make sure lang_code matches voice
    generator = pipeline(text, voice, speed)
    audios = []
    for _, _, audio in generator:
        audios.append(audio)
    audios = np.concatenate(audios)
    sf.write(audio_file, audios, sample_rate, bitrate_mode="VARIABLE")


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
        "--sample-rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help=f"Audio sample rate (default: {DEFAULT_SAMPLE_RATE})",
    )

    args = parser.parse_args()

    gen_audio(
        args.text,
        args.audio_file,
        voice=args.voice,
        speed=args.speed,
        sample_rate=args.sample_rate,
    )
    print(f"Audio saved to {args.audio_file}")


if __name__ == "__main__":
    main()
