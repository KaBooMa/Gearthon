from dataclasses import dataclass, field

from classes.Tweakable import Tweakable


@dataclass
class StringTweakable(Tweakable):
    initial_value: str = field(default='', metadata={'label': 'Initial Value'})
    multiline: bool = field(default=False, metadata={'label': 'Multiple Lines'})