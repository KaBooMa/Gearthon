from dataclasses import dataclass, field
from typing import List

from classes.LinkType import LinkType
from classes.Material import Material
from classes.Part import Part

@dataclass
class Mod:
    name: str = field(default='New Mod', metadata={'label': 'Name', 'hidden': True})
    description: str = field(default='', metadata={'label': 'Description'})
    parts: List[Part] = field(default_factory=list, metadata={'hidden': True})
    materials: List[Material] = field(default_factory=list, metadata={'hidden': True})
    link_types: List[LinkType] = field(default_factory=list, metadata={'hidden': True})