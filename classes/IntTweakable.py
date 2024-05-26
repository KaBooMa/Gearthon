from dataclasses import dataclass, field

from classes.Tweakable import Tweakable


@dataclass
class IntTweakable(Tweakable):
    initial_value: int = field(default=0, metadata={'label': 'Initial Value'})
    maximum: int = field(default=10, metadata={'label': 'Maximum'})
    minimum: int = field(default=0, metadata={'label': 'Minimum'})