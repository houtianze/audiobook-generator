import os
import zipfile

from rich import print

from audiobook_generator.defaults import *
from audiobook_generator.main import split_and_gen_audio


def str_to_bool(value):
    true_values = {"true", "1", "yes", "y", "on", "t"}
    false_values = {"false", "0", "no", "n", "off", "f"}

    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in true_values:
            return True
        elif value_lower in false_values:
            return False
    raise ValueError(f"Cannot convert '{value}' to a boolean.")


def convert_epub_to_audio(epub_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    split_and_gen_audio(
        epub_file,
        output_dir,
        voice=os.getenv("VOICE", DEFAULT_VOICE),
        speed=os.getenv("SPEED", DEFAULT_SPEED),
        format=os.getenv("FORMAT", DEFAULT_FORMAT),
        resume=str_to_bool(os.getenv("RESUME", str(DEFAULT_RESUME))),
        split_subsections=str_to_bool(
            os.getenv("SPLIT_SUBSECTIONS", str(DEFAULT_SPLIT_SUBSECTIONS))
        ),
    )


def process_epub_files(input_dir, output_dir, act):

    # Find all .epub files in the current directory
    epub_files = [file for file in os.listdir(input_dir) if file.endswith(".epub")]

    for epub_file in epub_files:
        epub_file = os.path.join(input_dir, epub_file)
        print(f"Processing {epub_file}...")
        act(epub_file, output_dir)


def zip_it(output_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)


def main():
    input_dir = os.path.dirname(os.getcwd())
    output_dir_name = os.environ.get("OUTPUT_DIR", "Audiobook")
    output_dir = os.path.join("..", output_dir_name)
    process_epub_files(input_dir, output_dir, convert_epub_to_audio)
    if os.path.exists(output_dir):
        zip_file_path = os.path.join(os.path.dirname(output_dir), f"{output_dir_name}.zip")
        zip_it(output_dir, zip_file_path)
    else:
        print(
            f"[blue]Output directory '{output_dir}' does not exist. Skipping zip and upload.[/blue]"
        )


if __name__ == "__main__":
    main()
