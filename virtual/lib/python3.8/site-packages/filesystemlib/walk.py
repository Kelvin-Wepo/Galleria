from pathlib import Path
from typing import Any, Callable, Iterator, Optional, Union
import logging
import os

logger = logging.getLogger(__name__)


def walk(
    path: Union[Path, os.DirEntry],
    *,
    maxdepth: Union[int, float] = float("inf"),
    sortkey: Optional[Callable[[Path], Any]] = None,
    strict: bool = False,
) -> Iterator[Union[Path, os.DirEntry]]:
    """
    Recursively walk filesystem, iterating into directories pre-order, depth-first.

    Set `maxdepth` to stop at some specified depth. E.g., `maxdepth=0` produces `path`
    and then stops; `maxdepth=1` iterates over `path` and (if its a directory) its
    children, but no further.

    Set `sortkey` to a function from a Path to a comparable value to sort children
    within each directory.

    Set `strict` to True to raise permissions errors when listing a directory's contents;
    by default such errors are logged (at "warning" level) but otherwise ignored.
    """
    yield path
    if maxdepth > 0 and not path.is_symlink() and path.is_dir():
        try:
            children = os.scandir(path)
            if sortkey:
                children = sorted(children, key=sortkey)
            for child in children:
                yield from walk(
                    child, maxdepth=maxdepth - 1, sortkey=sortkey, strict=strict
                )
        except PermissionError as exc:
            if strict:
                raise
            logger.warning("Could not descend into directory: %s", exc)
