from __future__ import annotations

from pathlib import Path
import shutil
from subprocess import run, PIPE
from tempfile import TemporaryDirectory

import goldpy
from jinja2 import FileSystemLoader
from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func

from typing import Dict, Any, Iterable

from .bibtex import bibtex_render
from . import schema


EXTRA_FILES = [
    'fontawesome.sty',
]


@markup_escape_func
def tex_escape(s):
    return (
        s.replace('&', r'\&')
         .replace('%', r'\%')
    )

def date(datetime, fmt: str) -> str:
    return datetime.strftime(fmt.replace('~','%'))


class Template(schema.Template):

    path: Path

    @classmethod
    def from_file(cls, path: Path) -> Template:
        spec = goldpy.eval_file(str(path / 'template.gold'))
        return cls.parse_obj({
            **spec,
            'path': path,
        })

    @property
    def files(self) -> Iterable[Path]:
        for filename in self.extra_files:
            yield self.path / filename

    @property
    def bibtex(self) -> Path:
        return self.path / self.bibtex_style


class Resume(schema.Resume):

    template: Template
    extra_path: Path

    @classmethod
    def from_file(cls, resume_path: Path, template_path: Path) -> Resume:
        template = Template.from_file(Path(__file__).parent / 'templates' / template_path)
        extra_path = Path(__file__).parent / 'extra'
        spec = goldpy.eval_file(str(resume_path))
        return cls.parse_obj({
            **spec,
            'template': template,
            'extra_path': extra_path,
        })

    def render(self, out: Path, mode: str, context: Dict[str, Any], debug: bool = False):
        assert mode in self.template.modes

        if mode == 'cover':
            assert self.cover

        env = DynAutoEscapeEnvironment(
            autoescape=True,
            escape_func=tex_escape,
            loader=FileSystemLoader(str(self.template.path)),
            block_start_string=r'\BLOCK{',
            block_end_string=r'}',
            variable_start_string=r'\VAR{',
            variable_end_string=r'}',
            comment_start_string=r'\#{',
            comment_end_string=r'}',
            line_statement_prefix=r'%%%',
            line_comment_prefix=r'%%#'
        )

        env.filters.update({
            'date': date,
        })

        context = dict(context)
        context.update(self)
        context.update({
            'fontpath': str(Path(__file__).parent / 'extra' / 'fonts') + '/',
        })

        if self.publications:
            context['publications'] = bibtex_render(
                self.template.bibtex,
                map(Path, self.publications.bibfiles),
                self.publications.keys,
                self.publications.boldnames,
            )

        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)

            if self.photo:
                shutil.copy(self.photo, tmp)

            for source in self.template.files:
                shutil.copy(source, tmp)

            for fn in EXTRA_FILES:
                shutil.copy(self.extra_path / fn, tmp)

            for filename in self.template.entrypoints:
                with open(tmp / filename, 'w') as f:
                    f.write(env.get_template(filename).render(**context))

            kwargs = {}
            if not debug:
                kwargs['stdout'] = kwargs['stderr'] = PIPE
            run(['latexmk', '-pdflua', '-interaction=nonstopmode', f'{mode}.tex'], cwd=tmp, **kwargs).check_returncode()
            shutil.copy(tmp / f'{mode}.pdf', out)
