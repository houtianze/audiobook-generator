import argparse
from os import environ

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline
from rich import print

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
    # 'z' => Mandarin Chinese: pip install misaki[zh]
    lang_code = voice[0]
    device = None
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        # To use MPS device, we need to set the environment variable PYTORCH_ENABLE_MPS_FALLBACK to 1,
        # Otherwise, you will see the following error:
        # NotImplementedError: The operator 'aten::angle' is not currently implemented for the MPS device.
        if "PYTORCH_ENABLE_MPS_FALLBACK" in environ and environ["PYTORCH_ENABLE_MPS_FALLBACK"]:
            print("[italic]Using MPS device with fallback.[/italic]")
            device = "mps"
        else:
            print(
                "[purple]"
                "environment variable 'PYTORCH_ENABLE_MPS_FALLBACK' is not defined and set to 1, "
                "please set it to 1 to use MPS device, otherwise CPU will be used instead, "
                "which is slower (but it still works nevertheless)."
                "[purple]"
            )
    pipeline = KPipeline(
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
