from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Dict, Iterator, Optional, Tuple, Union
import logging
import io

import exifread
import pyheif

logger = logging.getLogger(__name__)

TAG2NAME: Dict[int, str] = {
    tag: name_and_mapper[0] for tag, name_and_mapper in exifread.tags.EXIF_TAGS.items()
}
NAME2TAG: Dict[str, int] = {v: k for k, v in TAG2NAME.items()}


def _expand(tag_or_name: Union[int, str]) -> Tuple[int, str]:
    if isinstance(tag_or_name, int):
        tag = tag_or_name
        name = TAG2NAME[tag]
    else:
        name = tag_or_name
        tag = NAME2TAG[name]
    return tag, name


def _process_file(
    fh: BinaryIO,
    stop_tag: str = exifread.DEFAULT_STOP_TAG,
    details: bool = True,
    strict: bool = False,
    debug: bool = False,
    truncate_tags: bool = True,
):
    """
    ExifRead claims to handle HEIC (HEIF) images, but it can't handle mine. This is a
    wrapper that intercepts HEIC images and uses pyheif to extract the exif data, but
    otherwise hands over directly to ExifRead.
    """
    header = fh.read(12)
    if header[4:12] == b"ftypheic":
        fh.seek(0)
        heif_file = pyheif.read(fh)
        exif_data = next(
            item["data"] for item in heif_file.metadata if item["type"] == "Exif"
        )
        fh = io.BytesIO(exif_data[len(b"Exif\x00\x00") :])
    return exifread.process_file(
        fh,
        stop_tag=stop_tag,
        details=details,
        strict=strict,
        debug=debug,
        truncate_tags=truncate_tags,
    )


def read_tag_value(path: Path, tag_or_name: Union[int, str]) -> Optional[str]:
    tag, name = _expand(tag_or_name)
    with path.open("rb") as fp:
        hdr_tags = _process_file(fp, stop_tag=name)
        for ifd_tag in hdr_tags.values():
            if not isinstance(ifd_tag, bytes) and ifd_tag.tag == tag:
                return str(ifd_tag)
    return None


def _iter_tags(path: Path, details: bool = True) -> Iterator[Tuple[str, str]]:
    with path.open("rb") as fp:
        hdr_tags = _process_file(fp, details=details)
        for key, ifd_tag in hdr_tags.items():
            # strip the ifd_name prefix from each key
            sep_index = key.find(" ")
            if sep_index != -1:
                key = key[sep_index + 1 :]
            yield key, str(ifd_tag)


def read_tags(path: Path, details: bool = True) -> Dict[str, str]:
    return dict(_iter_tags(path, details=details))


def parse_exif_datetime(value: str) -> datetime:
    """
    Parse Exif datetime format ("YYYY:MM:DD HH:MM:SS") (no timezone).
    """
    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")


def read_datetime(path: Path) -> datetime:
    """
    Try to read and parse the "DateTimeOriginal" Exif tag from the image at `path`.
    If that fails (e.g., `path` is not an image, or there is no such tag),
    `stat` the file and return the birthtime (and if that fails, return the mtime).
    """
    try:
        return parse_exif_datetime(read_tag_value(path, "DateTimeOriginal"))
    except TypeError as exc:
        logger.debug("Could not read Exif data from Image (%s)", exc)
    logger.info("Falling back to filesystem metadata for %s", path)
    sr = path.stat()
    timestamp = getattr(sr, "st_birthtime", sr.st_mtime)
    return datetime.fromtimestamp(timestamp)
