import argparse

import soundfile as sf
from kokoro import KPipeline
# import torch


def gen_audio(text, audio_file, voice="af_heart", speed=1, sample_rate=22050):
    # 'a' => American English, ' => British English
    # 'j' => Japanese: pip install misaki[ja]
    # 'z' => Mandarin Chinese: pip install misaki[zh]
    lang_code = voice[0]
    pipeline = KPipeline(lang_code=lang_code, device='cuda')  # <= make sure lang_code matches voice
    generator = pipeline(text, voice, speed)
    for _, _, audio in generator:
        sf.write(audio_file, audio, sample_rate, bitrate_mode='VARIABLE')


def main():

    parser = argparse.ArgumentParser(description="Convert text to speech")
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("audio_file", help="Output audio filename")
    parser.add_argument(
        "--voice", default="af_heart", help="Voice to use (default: af_heart)"
    )
    parser.add_argument(
        "--speed", type=float, default=1.0, help="Speech speed (default: 1.0)"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=22050,
        help="Audio sample rate (default: 22050)",
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
