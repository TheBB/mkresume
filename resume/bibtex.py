from pathlib import Path

from typing import Iterable

from pybtex.bibtex import BibTeXEngine


def bibtex_render(style: Path, bibfiles: Iterable[Path], keys: Iterable[str], boldnames: Iterable[str] = []):
    text = BibTeXEngine().format_from_files(list(bibfiles), str(style.with_suffix('')), list(keys))
    assert text

    for name in boldnames:
        text = text.replace(name, '\\textbf{' + name + '}')

    return text
    # print(type(text))
    # print(text)
    # import sys
    # sys.exit(0)
