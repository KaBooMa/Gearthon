from dataclasses import dataclass, field

from classes.Tweakable import Tweakable


@dataclass
class FloatTweakable(Tweakable):
    initial_value: float = field(default=0.0, metadata={'label': 'Initial Value'})
    maximum: float = field(default=1.0, metadata={'label': 'Maximum'})
    minimum: float = field(default=0.0, metadata={'label': 'Minimum'})