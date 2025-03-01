import os

from bs4 import BeautifulSoup
from ebooklib import ITEM_COVER, ITEM_IMAGE, epub


class Chapterizer(object):
    def __init__(self, epub_path, output_dir):
        self.epub_path = epub_path
        self.output_dir = output_dir
        self.book = epub.read_epub(epub_path)
        self.chapter_index = 0
        if not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)

    def save_cover(self, item):
        cover_ext = ".jpg"
        if '.' in item.file_name:
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
        def extract_link(chapter):
            item = self.book.get_item_with_href(chapter.href.split("#")[0])
            if not item:
                print(f"Error: Could not find item with href {chapter.href}")
                exit(1)

            soup = BeautifulSoup(item.content, "html.parser")
            self.chapter_index += 1
            chapter_name = f"{self.chapter_index:03d} - {chapter.title}"
            # Sanitize filename to work on all operating systems
            # Remove characters not allowed in filenames and replace with underscores
            invalid_chars = r'<>:"/\|?*'
            file_name = ''.join(c if c not in invalid_chars else '_' for c in chapter_name)
            # Limit length to avoid issues on systems with filename length restrictions
            file_name = file_name[:240] + ".txt"
            with open(os.path.join(self.output_dir, file_name), "w") as f:
                f.write(soup.get_text())
            return file_name

        def extract_chapters(items):
            generated_files = []
            for c in items:
                if isinstance(c, epub.Link):
                    generated_files.append(extract_link(c))
                elif isinstance(c, tuple):
                    for sc in c:
                        if isinstance(sc, epub.Section):
                            generated_files.append(extract_link(sc))
            return generated_files

        self.chapter_index = 0
        self.extract_cover()
        return extract_chapters(self.book.toc)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert EPUB to text files per chapter and extract cover image."
    )
    parser.add_argument("epub_path", help="Path to the EPUB file")
    parser.add_argument("output_dir", help="Directory to save the output files")

    args = parser.parse_args()
    chapterizer = Chapterizer(args.epub_path, args.output_dir)
    chapterizer.chapterize()
