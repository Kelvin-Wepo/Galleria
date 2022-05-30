"""
This module is intended to be a private API, providing common functionality to other
modules that are part of the public API.
"""
from typing import Union
import os

# "\x1b[33m" => set foreground color to yellow
# "\x1b[39m" => reset foreground color to default
DRY_RUN_PREFIX = "\x1b[33m[dry-run]\x1b[39m "

# this is what Python calls a "path-like object" — "either a str or bytes object
# representing a path, or an object implementing the os.PathLike protocol"
Pathable = Union[bytes, str, os.PathLike]
