import logging
from pathlib import Path
from datetime import date

from typing import List, Optional, Union

import goldpy
from pydantic import BaseModel, Field


class Name(BaseModel):
    first: str
    last: str


class Dates(BaseModel):
    begin: date
    end: Optional[date]


class Experience(BaseModel):
    title: str
    organization: str
    location: str
    dates: Dates
    tasks: List[str]


class Education(BaseModel):
    degree: str
    institution: str
    location: str
    dates: Dates
    description: str


class Honor(BaseModel):
    role: str
    event: str
    location: str
    date: date


class Committee(BaseModel):
    role: str
    committee: str
    location: str
    dates: Union[date, Dates]


class Presentation(BaseModel):
    role: str
    title: str
    event: str
    date: date


class Project(BaseModel):
    title: str
    role: str
    subtitle: Optional[str]
    partners: List[str] = []
    dates: Dates
    description: str


class Publications(BaseModel):
    bibfiles: List[str]
    keys: List[str]
    boldnames: List[str] = []


class Section(BaseModel):
    title: str
    text: str


class Cover(BaseModel):
    recipient: str
    address: List[str]
    title: str
    opening: str
    closing: str
    attachments: List[str] = []
    sections: List[Section]


class Skill(BaseModel):
    title: str
    text: str


class Hobby(BaseModel):
    title: str
    text: str


class Resume(BaseModel):
    photo: Optional[str]
    name: Name
    positions: List[str]
    address: List[str]
    phone: str
    email: str

    cover: Optional[Cover]

    website: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    quote: Optional[str]
    summary: Optional[str]

    experience: List[Experience] = []
    education: List[Education] = []
    honors: List[Honor] = []
    committees: List[Committee] = []
    presentations: List[Presentation] = []
    projects: List[Project] = []
    publications: Optional[Publications]
    skills: List[Skill] = []
    hobbies: List[Hobby] = []


class Template(BaseModel):
    bibtex_style: str = Field(alias='bibtex-style')
    extra_files: List[str] = Field(alias='extra-files', default_factory=list)
    entrypoints: List[str] = []
    modes: List[str]
