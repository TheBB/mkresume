from pathlib import Path

from strictyaml import (
    Optional, Map, Seq, Str, Datetime,
    load, YAMLError, Validator
)

import treelog as log


TEMPLATE_SCHEMA = Map({
    'entrypoints': Seq(Str()),
    Optional('extra-files'): Seq(Str()),
    Optional('bibtex-style'): Str(),
})


RESUME_SCHEMA = Map({
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
        'dates': Map({
            'from': Datetime(),
            Optional('to'): Datetime(),
        }),
        'tasks': Seq(Str()),
    })),
    Optional('education'): Seq(Map({
        'degree': Str(),
        'institution': Str(),
        'location': Str(),
        'dates': Map({
            'from': Datetime(),
            Optional('to'): Datetime(),
        }),
        'description': Str(),
    })),
    Optional('honors'): Seq(Map({
        'role': Str(),
        'event': Str(),
        'location': Str(),
        'date': Datetime(),
    })),
    Optional('publications'): Map({
        'bibfiles': Seq(Str()),
        'keys': Seq(Str()),
        Optional('boldnames'): Seq(Str()),
    }),
    Optional('presentations'): Seq(Map({
        'role': Str(),
        'title': Str(),
        'event': Str(),
        'date': Datetime(),
    })),
    Optional('projects'): Seq(Map({
        'title': Str(),
        'role': Str(),
        Optional('subtitle'): Str(),
        Optional('partners'): Seq(Str()),
        'dates': Map({
            'from': Datetime(),
            Optional('to'): Datetime(),
        }),
        'description': Str(),
    })),
    Optional('committees'): Seq(Map({
        'role': Str(),
        'committee': Str(),
        'location': Str(),
        Optional('date'): Datetime(),
        Optional('dates'): Map({
            'from': Datetime(),
            Optional('to'): Datetime(),
        }),
    }))
})


def load_and_validate(text: str, path: Path, schema: Validator):
    try:
        return load(text, schema, label=path).data
    except YAMLError as err:
        log.error(err)
        raise

def load_template(filename: Path):
    with open(filename, 'r') as f:
        return load_and_validate(f.read(), filename, TEMPLATE_SCHEMA)

def load_resume(filename: Path):
    with open(filename, 'r') as f:
        return load_and_validate(f.read(), filename, RESUME_SCHEMA)
