from dataclasses import dataclass, field

from classes.Color import Color


@dataclass
class LinkType:
    uid: int = field(metadata={'hidden': True})
    display_name: str = field(default='New Link Type', metadata={'label': 'Display Name'})
    color: Color = field(default_factory=Color, metadata={'label': 'Color'})