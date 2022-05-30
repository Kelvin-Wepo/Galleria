from typing import Iterator
import plistlib

from xattr import xattr

from ..internal import Pathable

COLOR_MAPPING = [
    "None",  # 0
    "Gray",  # 1
    "Green",  # 2
    "Purple",  # 3
    "Blue",  # 4
    "Yellow",  # 5
    "Red",  # 6
    "Orange",  # 7
]
FINDER_INFO = "com.apple.FinderInfo"
METADATA_ITEM_USER_TAGS = "com.apple.metadata:_kMDItemUserTags"


def read_tags(path: Pathable) -> Iterator[str]:
    """
    Read color names and/or other tags from a file's extended attributes.

    It reads from both _kMDItemUserTags and FinderInfo so the results will probably
    repeat the most recently added color.
    """
    attrs = xattr(path)
    # attrs#has_key just calls attrs#get in a try-except, ignoring the result
    try:
        metadata_item_user_tags: bytes = attrs.get(METADATA_ITEM_USER_TAGS)
        for item in plistlib.loads(metadata_item_user_tags):
            if "\n" in item:
                color, _number = item.split("\n")
                # assert COLOR_MAPPING[int(_number)] == color
                yield color
            else:
                yield item
    except IOError:
        pass
    # FINDER_INFO only supports a single color, and seems to be whatever (color) tag was
    # most recently set (unless tags were added to a file with a pre-Mavericks tag?)
    try:
        finder_info: bytes = attrs.get(FINDER_INFO)
        # color resides in 10th byte
        color_byte = finder_info[9]
        # select bits 2 through 4 (where rightmost is bit 1) by
        # first dropping the lowest bit then ANDing with 0b111 (= 7)
        color_value = (color_byte >> 1) & 7
        yield COLOR_MAPPING[color_value]
    except IOError:
        pass
