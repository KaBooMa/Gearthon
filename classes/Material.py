from dataclasses import dataclass, field


@dataclass
class Material:
    uid: int = field(metadata={'hidden': True})
    display_name: str = field(default='New Material', metadata={'label': 'Display Name'})
    density: float = field(default=0.4, metadata={'label': 'Density'})
    strength: float = field(default=500, metadata={'label': 'Strength'})
    is_paintable: bool = field(default=False, metadata={'label': 'Paintable'})
    file_type: str = field(default='', metadata={'label': 'File Type', 'hidden': True})
    bounciness: float = field(default=0.2, metadata={'label': 'Bounciness'})
    dynamic_friction: float = field(default=0.5, metadata={'label': 'Dynamic Friction'})
    static_friction: float = field(default=0.7, metadata={'label': 'Static Friction'})