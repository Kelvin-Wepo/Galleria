import logging
import os
import shutil

from .errors import file_not_found, file_exists
from .internal import DRY_RUN_PREFIX, Pathable
from .makedirs import makedirs

logger = logging.getLogger(__name__)


def move(
    source: Pathable,
    target: Pathable,
    force: bool = False,
    parents: bool = True,
    *,
    dry_run: bool = False,
) -> Pathable:
    """
    Move `source` to `target` unless they already refer to the same (real)path.

    Set `force` to True to overwrite `target` if it exists; by default raise
    FileExistsError if `target` exists.

    Set `parents` to False to not auto-create any missing parent directories.

    Returns `target` (or if `dry_run=True`, returns `source`)
    """
    # short-circuit if source and target refer to the same thing
    # os.path.samefile(source, target) doesn't work because it calls os.stat on each argument
    if os.path.realpath(source) == os.path.realpath(target):
        return target
    logger.info(
        "%sMoving %r -> %r",
        DRY_RUN_PREFIX if dry_run else "",
        os.fspath(source),
        os.fspath(target),
    )
    if not os.path.exists(source):
        raise file_not_found(source)
    if os.path.exists(target) and not force:
        raise file_exists(target)
    if parents:
        makedirs(os.path.dirname(target), dry_run=dry_run)
    if not dry_run:
        try:
            os.rename(source, target)
        except OSError as exc:
            if exc.errno != 18:
                # re-raise any exceptions that aren't "Cross-device link" errors
                raise
            logger.debug(
                "Encountered %r error; falling back to shutil.move", exc.strerror
            )
            target = shutil.move(source, target)
        return target
    return source
