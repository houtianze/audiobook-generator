import os

from bs4 import BeautifulSoup
from ebooklib import ITEM_COVER, ITEM_IMAGE, epub
from rich import print

from .util import make_fs_safe


class Chapterizer(object):
    def __init__(self, epub_path, output_dir, bare_output):
        self.epub_path = epub_path
        self.output_dir = output_dir
        self.bear_output = bare_output

        self.book = epub.read_epub(epub_path)
        if not bare_output:
            title = self.book.title
            author = "Unknown"
            try:
                author = self.book.get_metadata("DC", "creator")[0][0]
            except:
                print(
                    f"[red]Failed to extract author name, using '{author}' instead.[/red]"
                )
            book_directory = f"{title} - {author}"
            book_directory = make_fs_safe(book_directory)
            self.output_dir = os.path.join(output_dir, book_directory)
        os.makedirs(self.output_dir, exist_ok=True)

        self.chapter_index = 0

    def save_cover(self, item):
        cover_ext = ".jpg"
        if "." in item.file_name:
            cover_ext = item.file_name.split(".")[-1]
        cover_path = os.path.join(self.output_dir, f"cover.{cover_ext}")
        with open(cover_path, "wb") as f:
            f.write(item.content)

    def extract_cover(self):
        """Extract cover image from the EPUB file."""
        # First try using the cover metadata
        cover_id = None

        # Look for cover in the metadata
        # for key, value in self.book.get_metadata().items():
        for key, value in self.book.metadata.items():
            if key.endswith("cover"):
                cover_id = value[0][0]
                break

        # If cover_id found, try to get that item
        if cover_id:
            cover_item = self.book.get_item_with_id(cover_id)
            if cover_item:
                self.save_cover(cover_item)
                return True

        # Fall back method: look for items with cover type
        for item in self.book.get_items():
            if item.get_type() == ITEM_COVER:
                self.save_cover(item)
                return True

        # Last resort: look for image with 'cover' in the name
        for item in self.book.get_items_of_type(ITEM_IMAGE):
            if "cover" in item.get_name().lower():
                self.save_cover(item)
                return True

        print("Could not find cover image")
        return False

    def chapterize(self):

        # Then extract chapters (keeping existing functionality)
        def _extract(chapter):
            item = self.book.get_item_with_href(chapter.href.split("#")[0])
            if not item:
                print(f"Error: Could not find item with href {chapter.href}")
                exit(1)

            soup = BeautifulSoup(item.content, "html.parser")
            self.chapter_index += 1
            chapter_type = "Chapter" if isinstance(chapter, epub.Link) else "Section"
            chapter_name = (
                f"{self.chapter_index:03d} - {chapter_type} - {chapter.title}"
            )
            file_name = make_fs_safe(chapter_name)
            # Limit length to avoid issues on systems with filename length restrictions
            file_name = file_name[:240] + ".txt"
            file_name = os.path.join(self.output_dir, file_name)
            with open(file_name, "w", encoding="utf-8") as f:
                text = soup.get_text()
                f.write(text)
            return file_name

        def extract_chapters(items):
            extracted_files = []
            # DFS to flatten the nested chapters
            if isinstance(items, (tuple, list)):
                for item in items:
                    extracted_files.extend(extract_chapters(item))
            else:
                extracted_files.append(_extract(items))
            return extracted_files

        self.chapter_index = 0
        self.extract_cover()
        extracted_files = extract_chapters(self.book.toc)
        self.chapter_index = 0
        return self.output_dir, extracted_files


if __name__ == "__main__":
    import argparse

    from .defaults import *

    parser = argparse.ArgumentParser(
        description="Convert EPUB to text files per chapter and extract cover image."
    )
    parser.add_argument("epub_path", help="Path to the EPUB file")
    parser.add_argument("output_dir", help="Directory to save the output files")

    args = parser.parse_args()
    chapterizer = Chapterizer(args.epub_path, args.output_dir)
    chapterizer.chapterize()
