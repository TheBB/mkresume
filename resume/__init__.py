from pathlib import Path
import shutil
from subprocess import run, PIPE
from tempfile import TemporaryDirectory

from jinja2 import FileSystemLoader
from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func

from typing import Dict, Any, List, Tuple

from .schema import load_and_validate


EXTRA_FILES = [
    'fontawesome.sty',
]


@markup_escape_func
def tex_escape(s):
    return (
        s.replace('&', r'\&')
         .replace('%', r'\%')
    )


class Resume:

    def __init__(self, path: Path):
        self.template_path = Path(__file__).parent / 'templates'
        self.extra_path = Path(__file__).parent / 'extra'

        with open(path) as f:
            self.spec = load_and_validate(f.read(), path)

    def render(self, context: Dict[str, Any], template: str, debug: bool = False):
        template_path = self.template_path / template

        env = DynAutoEscapeEnvironment(
            autoescape=True,
            escape_func=tex_escape,
            loader=FileSystemLoader(str(template_path)),
            block_start_string=r'\BLOCK{',
            block_end_string=r'}',
            variable_start_string=r'\VAR{',
            variable_end_string=r'}',
            comment_start_string=r'\#{',
            comment_end_string=r'}',
            line_statement_prefix=r'%%%',
            line_comment_prefix=r'%%#'
        )

        entry_pts: List[Tuple[str, str]] = []
        with open(template_path / 'entrypts') as f:
            for line in f:
                args = line.split()
                if len(args) == 1:
                    entry_pts.append((args[0], args[0]))
                else:
                    entry_pts.append((args[0], args[1]))

        context = dict(context)
        context.update(self.spec)
        context.update({
            'fontpath': str(Path(__file__).parent / 'extra' / 'fonts') + '/',
        })

        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)

            for src, tgt in entry_pts:
                with open(tmp / tgt, 'w') as f:
                    f.write(env.get_template(src).render(**context))

            for fn in EXTRA_FILES:
                shutil.copy(self.extra_path / fn, tmp)

            kwargs = {}
            if not debug:
                kwargs['stdout'] = kwargs['stderr'] = PIPE
            run(['latexmk', '-pdflua', '-interaction=nonstopmode', 'resume.tex'], cwd=tmp, **kwargs).check_returncode()
            shutil.copy(tmp / 'resume.pdf', '.')
