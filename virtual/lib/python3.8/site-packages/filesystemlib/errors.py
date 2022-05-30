from errno import ENOENT, EEXIST, ENOTDIR
import os

from .internal import Pathable


def file_not_found(path: Pathable) -> FileNotFoundError:
    "Create proper FileNotFoundError instance"
    return FileNotFoundError(ENOENT, os.strerror(ENOENT), os.fspath(path))


def file_exists(path: Pathable) -> FileExistsError:
    "Create proper FileExistsError instance"
    return FileExistsError(EEXIST, os.strerror(EEXIST), os.fspath(path))


def not_a_directory(path: Pathable) -> FileExistsError:
    "Create proper NotADirectoryError instance"
    return NotADirectoryError(ENOTDIR, os.strerror(ENOTDIR), os.fspath(path))
