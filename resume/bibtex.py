from pathlib import Path

from typing import Iterable

from pybtex.bibtex import BibTeXEngine


def bibtex_render(style: Path, bibfiles: Iterable[Path], keys: Iterable[str]):
    return BibTeXEngine().format_from_files(list(bibfiles), str(style.with_suffix('')), list(keys))
