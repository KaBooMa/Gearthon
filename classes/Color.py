from dataclasses import dataclass, field


@dataclass
class Color:
    r: float = field(default=1.0, metadata={'label': 'Red'})
    g: float = field(default=1.0, metadata={'label': 'Green'})
    b: float = field(default=1.0, metadata={'label': 'Blue'})
    a: float = field(default=1.0, metadata={'label': 'Alpha'})