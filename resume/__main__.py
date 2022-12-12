import logging
from pathlib import Path
import sys
import traceback

from typing import Optional

import click
import click_pathlib
import rich.logging

from . import Resume


@click.command()

# Logging and verbosity
@click.option('--debug', 'verbosity', flag_value='debug')
@click.option('--info', 'verbosity', flag_value='info', default=True)
@click.option('--warning', 'verbosity', flag_value='warning')
@click.option('--error', 'verbosity', flag_value='error')
@click.option('--critical', 'verbosity', flag_value='critical')

@click.option('--template', default='awesome-resume')

@click.option('--resume', 'mode', flag_value='resume', default=True)
@click.option('--cover', 'mode', flag_value='cover')

@click.option('--out', type=click_pathlib.Path(writable=True, dir_okay=False), default=None)

@click.argument('path', type=click_pathlib.Path(exists=True, readable=True, dir_okay=False), default='resume.gold')

def main(verbosity: str, template: str, mode: str, path: Path, out: Optional[Path]):
    if out is None:
        out = Path(f'{mode}.pdf')

    logging.basicConfig(
        level=verbosity.upper(),
        format='%(message)s',
        datefmt='[%X]',
        handlers=[rich.logging.RichHandler(show_path=False, show_time=False)],
        force=True,
    )

    blocks = [
        'summary',
        'experience',
        'education',
        'skills',
        'honors',
        # 'publications',
        # 'presentations',
        'projects',
        'committees',
        'hobbies',
    ]

    try:
        Resume.from_file(path, template).render(out, mode, {'blocks': blocks}, verbosity == 'debug')
    except Exception as err:
        if verbosity == 'debug':
            traceback.print_exc()
        else:
            logging.critical(err)
            sys.exit(1)
