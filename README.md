audiobook-generator - Generate audiobooks (epub) from ebooks (one mp3 per chapter)
==================================================================================

## Flow
```mermaid
graph TD;
    A[Input file] --> B["Convert to text and chapterize (Optionally extract out the cover image)"];
    B --> C[Transform to audio files];
```

## Usage

### Prerequisites
- Python 3.10+ (This program was tested on 3.12)
- (Optional) Install [espeak-ng](https://github.com/espeak-ng/espeak-ng) (On Debian/Ubuntu, run `apt install -y espeak-ng`)
- (Development only) [uv](https://github.com/astral-sh/uv)

### For End Users
- You don't need to clone this repository and you can install either way:
  - Using `pip`: `python -m pip install audiobook-generator` (virtual environment highly recommended)
  - Using `pipx`: `pipx install audiobook-generator`
  - **NOTE** For Windows users, there is one extra step needed to make cuda(Nvidia) GPU is used when available:
    - If using `pip` and virtual environment, run this after the above `pip install` command (*with the virtual environment activated first*)
      - `pip install torch --index-url https://download.pytorch.org/whl/cu124 --force`
    - If using `pipx`, run this command instead:
      - `pipx runpip audiobook-generator install torch --index-url https://download.pytorch.org/whl/cu124 --force`
    - Technical details on why this is needed is described at [the "Why you need that extra pip install step for Windows?" section](#why-you-need-that-extra-pip-install-step-for-windows).
- Convert your epub file to audiobooks via the command
  - `abg <epub path> <audio output directory>`
- If you want to see all the command line switches, just run `abg -h`

### For Development
- This program uses [`uv`](https://github.com/astral-sh/uv) for dependency management and execution in development, install it first if you haven't done so.
- To run the program from its source:
  - Clone this repository and `cd` inside.
  - (Do it ONCE only at the first time) Run `uv sync` to create the virtual environment in the `.env` directory and download all the dependencies.
  - Then run the following command
    - `uv run -m audiobook_generator.main ...`

### CPU or GPU?
The selection to run the model on CPU or GPU is automatic, meaning:
- On Windows/WSL/Linux, If you have Nvidia graphic card with the driver properly installed, the model will be loaded to GPU (cuda) and executed, otherwise, the CPU is used (which is slower compared to GPU)
- On Mac, you need to set the environment variable `PYTORCH_ENABLE_MPS_FALLBACK=1` for it to run on GPU (because at the time of writing, the MPS support in PyTorch is not complete and it won't work without the CPU fallback), otherwise it will run on CPU.

### Why you need that extra pip install step for Windows?
(Thanks to @notimp for spotting [this issue](#4).)

If you go to [pytorch](https://pytorch.org/get-started/locally/), you will see that to install pytorch (only) on Windows, you need to specify the `--index-url` parameter (e.g. `pip3 install torch --index-url https://download.pytorch.org/whl/cu124`). When using `uv` for development, this is handled by [this section](https://github.com/houtianze/audiobook-generator/blob/9df750d943806ff89d55e78e21114878bb300822/pyproject.toml#L29-L37) of the `pyproject.toml` file:

```toml
[tool.uv.sources]
torch = [
    { index = "pytorch-cu124", marker = "sys_platform == 'win32'" },
]

[[tool.uv.index]]
name = "pytorch-cu124"
url = "https://download.pytorch.org/whl/cu124"
explicit = true
```

So running under `uv` in development, the torch dependency are installed correctly. However when it's packaged and published to [PyPI](https://pypi.org), it seems that this special specification of the torch index part is not respected by `pip` and when you run `pip` (or `pipx`) install, it just runs `pip install torch` on Windows without that `--index-url` parameter, which installs a version that doesn't support cuda/GPU. Currently I don't see how I can resolve this in packaging as I guess python package specification _may_ not support different dependency installation parameters on different platforms, or maybe I haven't digged deep enough. So for now, this extra step is required to install the correct version of torch on Windows.

## Misc

- You can use [this epub](https://github.com/daisy/epub-accessibility-tests/releases/download/fundamental-2.0/Fundamental-Accessibility-Tests-Basic-Functionality-v2.0.0.epub) for testing:

