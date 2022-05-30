from datetime import datetime
from itertools import groupby
from pathlib import Path
from typing import List, Tuple
import logging

from colorama import Fore
from filesystemlib import makedirs, move

from .metadata import read_datetime

logger = logging.getLogger(__name__)

DRY_RUN_PREFIX = f"{Fore.YELLOW}[dry-run]{Fore.RESET} "


def by_month(
    sources: List[Path],
    target: Path,
    dir_format: str = "%Y%m%d",
    *,
    dry_run: bool = False,
):
    """
    Group files by month, and move the files in each group into directories in `target`.
    Directories are created if needed, and are named according to the strftime-
    compatible `dir_format`, which is applied to the newest (last) photo in the group.
    """
    logger.info("Organizing %d sources into %s", len(sources), target)
    timestamps = [read_datetime(source) for source in sources]

    def key(source_timestamp: Tuple[Path, datetime]):
        _, timestamp = source_timestamp
        return timestamp.year, timestamp.month

    for _, group in groupby(sorted(zip(sources, timestamps), key=key), key=key):
        # group is a list of (source, timestamp) pairs
        group_sources, group_timestamps = zip(*group)
        max_timestamp = max(group_timestamps)
        group_dir = target / max_timestamp.strftime(dir_format)
        makedirs(group_dir, dry_run=dry_run)
        for group_source in group_sources:
            move(group_source, group_dir / group_source.name, dry_run=dry_run)
