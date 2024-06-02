from dataclasses import dataclass, field
from typing import List

from classes.Attachment import Attachment
from classes.BooleanTweakable import BooleanTweakable
from classes.FloatTweakable import FloatTweakable
from classes.InputActionTweakable import InputActionTweakable
from classes.IntTweakable import IntTweakable
from classes.JoystickTweakable import JoystickTweakable
from classes.Link import Link
from classes.StringTweakable import StringTweakable
from classes.Vector3 import Vector3

@dataclass
class Part:
    uid: int = field(metadata={'hidden': True})
    display_name: str = field(default='New Part', metadata={'label': 'Display Name'})
    category: str = field(default='Blocks', metadata={'label': 'Category', 'options': [
        'Aero',
        'Blocks',
        'Bodies',
        'Brakes & Clutches',
        'Checkpoints',
        'Connectors',
        'Control Wheels',
        'Electronics',
        'Gears',
        'Lights',
        'Linear Actuators',
        'Motors',
        'Power',
        'Props',
        'Pulleys',
        'Seats',
        'Suspension',
        'Wheels',
    ]})
    mass: float = field(default=1, metadata={'label': 'Mass (kgs)'})
    is_paintable: bool = field(default=False, metadata={'label': 'Paintable'})
    is_swappable_material: bool = field(default=False, metadata={'label': 'Swappable Material'})
    mesh_collider: bool = field(default=False, metadata={'label': '(EXPERIMENTAL) Use Mesh Collider'})
    custom_collider: bool = field(default=False, metadata={'label': '(EXPERIMENTAL) Custom Collider'})
    custom_collider_position: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0), metadata={'label': 'Custom Collider Position'})
    script: str = field(default='', metadata={'label': 'Script', 'hidden': True})
    int_tweakables: List[IntTweakable] = field(default_factory=list, metadata={'hidden': True})
    string_tweakables: List[StringTweakable] = field(default_factory=list, metadata={'hidden': True})
    joystick_tweakables: List[JoystickTweakable] = field(default_factory=list, metadata={'hidden': True})
    inputaction_tweakables: List[InputActionTweakable] = field(default_factory=list, metadata={'hidden': True})
    float_tweakables: List[FloatTweakable] = field(default_factory=list, metadata={'hidden': True})
    boolean_tweakables: List[BooleanTweakable] = field(default_factory=list, metadata={'hidden': True})
    attachments: List[Attachment] = field(default_factory=list, metadata={'hidden': True})
    links: List[Link] = field(default_factory=list, metadata={'hidden': True})