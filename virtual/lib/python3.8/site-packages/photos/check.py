from pathlib import Path
from typing import Iterator, List
import logging
import re
import sys

from colorama import Fore

from . import IMAGE_SUFFIXES

logger = logging.getLogger(__name__)

TOP_CHILD_NAME_PATTERN = r"^\d{8}-\w+(--[0-9A-Za-z]+)?$"


def iter_name_violations(path: Path) -> Iterator[str]:
    """
    Check that `path` has a name matching the pattern:
       YYYYMMDD-Some_Words(--OptionalEndWords)

    `path` should be an immediate child of the "top" directory.
    """
    logger.debug("Checking for name violations in %s", path)
    m = re.match(TOP_CHILD_NAME_PATTERN, path.name)
    if not m:
        yield f"{Fore.YELLOW}{path.name}{Fore.RESET} does not match"


def iter_contents_violations(directory: Path) -> Iterator[str]:
    """
    Check that `directory` has children that all match these criteria:
    * they are files (no nested directories)
    * they have a image-like suffix

    `directory` should be an immediate child of the "top" directory.
    """
    logger.debug("Checking for contents violations in %s", directory)
    if not directory.is_dir():
        yield f"{Fore.YELLOW}{directory.name}{Fore.RESET} is not a directory"
    else:
        children = sorted(directory.iterdir())
        subdirectories = [child for child in children if child.is_dir()]
        if subdirectories:
            yield (
                f"{Fore.YELLOW}{directory.name}{Fore.RESET} contains subdirectories: "
                f"{' '.join(subdirectory.name for subdirectory in subdirectories)}"
            )
        nonimage_files = [
            child
            for child in children
            if not child.is_dir() and child.suffix not in IMAGE_SUFFIXES
        ]
        if nonimage_files:
            yield (
                f"{Fore.YELLOW}{directory.name}{Fore.RESET} contains non-images: "
                f"{' '.join(nonimage_file.name for nonimage_file in nonimage_files)}"
            )


def print_all_violations(children: List[Path]):
    status = 0

    print(f"Checking that each child matches pattern: /{TOP_CHILD_NAME_PATTERN}/")
    violations = []
    for child in children:
        for violation in iter_name_violations(child):
            print(f"  {violation}")
            violations.append(violation)
    if violations:
        print(f"{Fore.RED}Pattern check found {len(violations)} violations{Fore.RESET}")
        status = 65  # EX_DATAERR

    print("Checking that each child contains no non-images or nested directories")
    violations = []
    for child in children:
        for violation in iter_contents_violations(child):
            print(f"  {violation}")
            violations.append(violation)
    if violations:
        print(f"{Fore.RED}Content check found {len(violations)} violations{Fore.RESET}")
        status = 65  # EX_DATAERR

    sys.exit(status)
