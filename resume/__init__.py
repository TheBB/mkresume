from pathlib import Path
import shutil
from subprocess import run, PIPE
from tempfile import TemporaryDirectory

from jinja2 import FileSystemLoader
from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func

from typing import Dict, Any, List, Tuple, Iterable, Optional

from .bibtex import bibtex_render
from .schema import load_template, load_resume


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


class Template:

    path: Path
    spec: Dict

    def __init__(self, path: Path):
        self.path = path
        self.spec = load_template(path / 'template.yaml')

    @property
    def entrypoints(self) -> Iterable[str]:
        return self.spec.get('entrypoints', [])

    @property
    def files(self) -> Iterable[Path]:
        for filename in self.spec.get('extra-files', []):
            yield self.path / filename

    @property
    def bibtex_style(self) -> Path:
        return self.path / self.spec['bibtex-style']


class Resume:

    template: Template

    def __init__(self, resume_path: Path, template_path: Path):
        self.template = Template(Path(__file__).parent / 'templates' / template_path)
        self.extra_path = Path(__file__).parent / 'extra'
        self.spec = load_resume(resume_path)

    def render(self, context: Dict[str, Any], debug: bool = False):
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
        context.update(self.spec)
        context.update({
            'fontpath': str(Path(__file__).parent / 'extra' / 'fonts') + '/',
        })

        if 'publications' in context:
            context['publications'] = bibtex_render(
                self.template.bibtex_style,
                map(Path, context['publications']['bibfiles']),
                context['publications']['keys']
            )

        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)

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
            run(['latexmk', '-pdflua', '-interaction=nonstopmode', 'resume.tex'], cwd=tmp, **kwargs).check_returncode()
            shutil.copy(tmp / 'resume.pdf', '.')
