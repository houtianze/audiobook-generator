from chapterizer import get_toc, chapterize

def main():
    epub_path = 'C:/Users/ibic/Downloads/Fundamental-Accessibility-Tests-Basic-Functionality-v2.0.0.epub'
    output_dir = 'C:/Users/ibic/AppData/Local/Temp/gen-audio-test'

    toc = get_toc(epub_path)
    for c in toc:
        print(c)
    # chapterize(epub_path, output_dir)


if __name__ == "__main__":
    main()
