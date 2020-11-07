from pathlib import Path

from strictyaml import (
    Optional, Map, Seq, Str,
    load, YAMLError,
)

import treelog as log


SCHEMA = Map({
    'name': Map({'first': Str(), 'last': Str()}),
    'positions': Seq(Str()),
    'address': Str(),
    'phone': Str(),
    'email': Str(),
    Optional('website'): Str(),
    Optional('github'): Str(),
    Optional('linkedin'): Str(),
    Optional('quote'): Str(),
    Optional('summary'): Str(),
    Optional('experience'): Seq(Map({
        'title': Str(),
        'organization': Str(),
        'location': Str(),
        'dates': Map({'from': Str(), Optional('to'): Str()}),
        'tasks': Seq(Str()),
    })),
    Optional('honors'): Seq(Map({
        'role': Str(),
        'event': Str(),
        'location': Str(),
        'date': Str(),
    }))
})


def load_and_validate(text: str, path: Path):
    try:
        return load(text, SCHEMA, label=path).data
    except YAMLError as err:
        log.error(err)
        raise
