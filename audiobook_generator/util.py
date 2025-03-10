import importlib
import subprocess
from os import environ


# https://stackoverflow.com/a/67504607/404271
def is_nvidia_available():
    try:
        subprocess.check_output("nvidia-smi")
        return True
    except:  # this command not being found can raise quite a few different errors depending on the configuration
        return False


def is_mps_supported():
    torch = importlib.import_module("torch")

    return torch.backends.mps.is_available() and torch.backends.mps.is_built()


def is_mps_fallback_enabled():
    return (
        "PYTORCH_ENABLE_MPS_FALLBACK" in environ
        and environ["PYTORCH_ENABLE_MPS_FALLBACK"]
    )


def make_fs_safe(text):
    """
    Convert a string to a file system safe string by replacing or removing invalid characters.

    Args:
        text (str): The input string to convert

    Returns:
        str: A file system safe version of the input string
    """
    # Characters that are problematic in file systems
    invalid_chars = '<>:"/\\|?*'

    # Replace invalid characters with underscore
    safe_text = "".join(c if c not in invalid_chars else "_" for c in text)

    # Trim leading/trailing spaces and periods (problematic in some file systems)
    safe_text = safe_text.strip(" .")

    # Ensure the string is not empty or just underscores
    if not safe_text or safe_text.strip("_") == "":
        safe_text = "unnamed"

    return safe_text
