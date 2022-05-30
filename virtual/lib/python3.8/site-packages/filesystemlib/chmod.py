import logging
import os

from .internal import DRY_RUN_PREFIX, Pathable

logger = logging.getLogger(__name__)


def chmod(path: Pathable, mode: int = 0o644, *, dry_run: bool = False):
    """
    Set the access permissions of the file/directory at `path` to `mode`.

    Checks first if the existing mode already matches the given mode,
    in which case it does nothing.
    """
    current_mode = os.stat(path).st_mode & 0o777
    # short-circuit if current mode matches
    if current_mode != mode:
        logger.info(
            "%sChanging file mode of %r: %o -> %o",
            DRY_RUN_PREFIX if dry_run else "",
            os.fspath(path),
            current_mode,
            mode,
        )
        if not dry_run:
            os.chmod(path, mode)
