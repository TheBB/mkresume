from pathlib import Path
import sys
import traceback

import click
import click_pathlib
import treelog as log

from . import Resume


class RichOutputLog(log.RichOutputLog):

    def __init__(self, stream):
        super().__init__()
        self.stream = stream

    def write(self, text, level):
        message = ''.join([self._cmap[level.value], text, '\033[0m\n', self._current])
        click.echo(message, file=self.stream, nl=False)


@click.command()

# Logging and verbosity
@click.option('--debug', 'verbosity', flag_value='debug')
@click.option('--info', 'verbosity', flag_value='info', default=True)
@click.option('--user', 'verbosity', flag_value='user')
@click.option('--warning', 'verbosity', flag_value='warning')
@click.option('--error', 'verbosity', flag_value='error')
@click.option('--rich/--no-rich', default=True)

@click.argument('path', type=click_pathlib.Path(exists=True, readable=True, dir_okay=False), default='resume.yaml')
@click.argument('template', default='awesome')

def main(verbosity: str, rich: bool, path: Path, template: str):
    if rich:
        logger = RichOutputLog(sys.stdout)
    else:
        logger = log.TeeLog(
            log.FilterLog(log.StdoutLog(), maxlevel=log.proto.Level.user),
            log.FilterLog(log.StderrLog(), minlevel=log.proto.Level.warning),
        )
    log.current = log.FilterLog(logger, minlevel=getattr(log.proto.Level, verbosity))

    blocks = [
        'summary',
        'experience',
        'honors',
    ]

    try:
        Resume(path).render({'blocks': blocks}, template, verbosity == 'debug')
    except Exception as err:
        if verbosity == 'debug':
            traceback.print_exc()
        else:
            print(err)
            sys.exit(1)
