import argparse
import importlib
import os
import re

from rich import print

from audiobook_generator.util import (
    is_mps_fallback_enabled,
    is_mps_supported,
    is_nvidia_available,
)

from .chapterizer import Chapterizer
from .defaults import *
from .tts import gen_audio


def split_and_gen_audio(
    epub_path,
    output_dir,
    voice=DEFAULT_VOICE,
    speed=DEFAULT_SPEED,
    format=DEFAULT_FORMAT,
    resume=DEFAULT_RESUME,
    bare_output=DEFAULT_BARE_OUTPUT,
):
    chapterizer = Chapterizer(epub_path, output_dir, bare_output)
    generated_text_files = chapterizer.chapterize()

    for text_file in generated_text_files:
        text = ""
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
        audio_file = re.sub(r"\.txt$", f".{format}", text_file)
        if resume and os.path.exists(audio_file):
            print(f"Skipping {audio_file} as it already exists")
            continue
        gen_audio(text, audio_file, voice, speed)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate audio from EPUB file")
    parser.add_argument("epub_path", type=str, help="Path to the EPUB file")
    parser.add_argument(
        "output_dir", type=str, help="Directory to save the output audio files"
    )
    parser.add_argument(
        "-v",
        "--voice",
        type=str,
        default=DEFAULT_VOICE,
        help=f"Voice to use for TTS. (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help=f"Speed of the TTS. (default: {DEFAULT_SPEED})",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default=DEFAULT_FORMAT,
        help=f"Format (file extension) of the generated audio files. (default: {DEFAULT_FORMAT})",
    )
    parser.add_argument(
        "-r",
        "--resume",
        type=bool,
        default=True,
        help=(
            "Whether to skip audio generation if the audio file already exists in the output directory "
            "(mainly when some previous run was interrupted). "
            "If False, any existing audio files generated previously will be overwritten. "
            "This applies only to audio files (mp3), where text files are always overwritten "
            f"as they are quite fast to generate. (default: {DEFAULT_RESUME})"
        ),
    )
    parser.add_argument(
        "-b",
        "--bare-output",
        type=bool,
        default=DEFAULT_BARE_OUTPUT,
        help=(
            "Whether to directly create files in the output directory specified. "
            "If false, a sub directory of the format 'Title - Author' will be created inside the output directory, "
            f"where all the file are created. (default: {DEFAULT_RESUME})"
        ),
    )
    return parser.parse_args()


def check_system():
    torch = importlib.import_module("torch")

    if os.name == "nt" and is_nvidia_available() and not torch.cuda.is_available():
        print(
            "[red]"
            "PyTorch installed does not support CUDA, to be able to use CUDA, "
            "please run the following command once and rerun this program:\n"
            "- (If using pip) "
            "pip install torch --index-url https://download.pytorch.org/whl/cu124 --force\n"
            "- (If using pipx) "
            "pipx runpip audiobook-generator install torch --index-url https://download.pytorch.org/whl/cu124 --force\n"
            "For more information, please refer to: "
            "https://github.com/houtianze/audiobook-generator/?tab=readme-ov-file#for-end-users\n"
            "[/red]"
        )

    if is_mps_supported() and not is_mps_fallback_enabled():
        # To use MPS device, we need to set the environment variable PYTORCH_ENABLE_MPS_FALLBACK to 1,
        # Otherwise, you will see the following error:
        # NotImplementedError: The operator 'aten::angle' is not currently implemented for the MPS device.
        print(
            "[purple]"
            "Environment variable 'PYTORCH_ENABLE_MPS_FALLBACK' is not defined as 1, "
            "please set it to 1 to use MPS, otherwise CPU will be used instead, "
            "which is slower (but still works nevertheless)."
            "[purple]"
        )


def main():
    args = parse_args()
    check_system()
    split_and_gen_audio(
        epub_path=args.epub_path,
        output_dir=args.output_dir,
        voice=args.voice,
        speed=args.speed,
        format=args.format,
        resume=args.resume,
        bare_output=args.bare_output,
    )
    print(
        (
            f"[bold green]All done. Audio files (along with the extracted text files) from '{args.epub_path}' are saved in '{args.output_dir}', "
            "chapter by chapter, along with the cover image (if any).[/bold green]"
        )
    )


if __name__ == "__main__":
    main()
