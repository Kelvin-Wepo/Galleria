from pathlib import Path

__version__ = None

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("photos").version
except Exception:
    pass

IMAGE_SUFFIXES = frozenset(
    suffix
    for canonical_suffix in (
        # typical
        ".jpg",
        ".heic",
        ".png",
        ".tif",
        ".bmp",
        # raw
        ".cr2",
        ".xmp",
        ".aae",
        # documents
        ".pal",
        ".psp",
        ".psd",
        ".pdf",
        # movies
        ".thm",
        ".gif",
        ".mov",
        ".mpg",
        ".mp4",
        ".avi",
    )
    for suffix in (canonical_suffix, canonical_suffix.upper())
)


def is_image(path: Path) -> bool:
    """
    Simple predicate to test whether `path`'s suffix (extension) looks like an image.
    """
    return path.suffix in IMAGE_SUFFIXES
