from pathlib import Path
from typing import List
import logging

import click

from . import __version__
from .check import print_all_violations
from .organize import by_month

logger = logging.getLogger("photos")


@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
def cli(verbose: int):
    logging_format = "%(asctime)14s %(levelname)-7s %(name)s - %(message)s"
    logging_level = logging.WARNING - (verbose * 10)
    logging_level_name = logging.getLevelName(logging_level)
    logging.basicConfig(format=logging_format, level=logging_level)
    logging.debug("Set logging level to %s [%d]", logging_level_name, logging_level)


@cli.command()
@click.argument("top", type=click.Path(exists=True, file_okay=False))
def check(top: str):
    """
    Check photos' organizational structure.

    Prints each violation as they are detected and summarizes by group at the end.
    """
    top = Path(top)
    logger.info("Using %s as top", top)
    children = sorted(top.iterdir(), key=lambda path: path.as_posix().casefold())
    logger.info("Found %d children", len(children))
    print_all_violations(children)
    logger.info("Done!")


@cli.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Destination",
)
@click.option(
    "-f",
    "--format",
    type=str,
    default="%Y%m%d",
    show_default=True,
    help="Format for new directories",
)
@click.option(
    "-n", "--dry-run", is_flag=True, help="Don't do anything, just log planned changes"
)
def organize_by_month(paths: List[str], output: str, format: str, dry_run: bool):
    """
    Reorganize photos by month.
    """
    sources = [Path(path) for path in paths]
    target = Path(output)
    logger.info("Organizing %d paths into %s", len(sources), target)
    by_month(sources, target, dir_format=format, dry_run=dry_run)
    logger.info("Done!")


main = cli.main


if __name__ == "__main__":
    main()
