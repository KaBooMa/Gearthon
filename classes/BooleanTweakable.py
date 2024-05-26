from dataclasses import dataclass, field

from classes.Tweakable import Tweakable


@dataclass
class BooleanTweakable(Tweakable):
    initial_value: bool = field(default=False, metadata={'label': 'Initial Value'})