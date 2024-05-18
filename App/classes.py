from dataclasses import dataclass, field
from typing import List, Optional, Type

@dataclass
class Vector3Int:
    x: int
    y: int
    z: int


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Attachment:
    name: str = field(default='', metadata={'label': 'Name'})
    attachment_flags: List[str] = field(
        default_factory=lambda: [], 
        metadata={
            'label': 'Attachment Flags', 
            'options': [
                'linear_bearing', 
                'rotary_bearing', 
                'constant_velocity_joint', 
                'fixed', 
                'knuckle_joint', 
                'linear_rotary_bearing', 
                'spherical_bearing'
            ], 
            'multiselect': True
        })
    alignment_flags: List[str] = field(
        default_factory=lambda: [], 
        metadata={
            'label': 'Alignment Flags',
            'options': [
                'clamp_180', 
                'clamp_90', 
                'is_bidirectional', 
                'is_female', 
                'is_interior', 
                'is_part_pairing_limited'
            ],
            'multiselect': True
        })
    position: Vector3 = field(default='', metadata={'label': 'Position'})
    orientation: Vector3 = field(default='', metadata={'label': 'Orientation'})
    size: Vector3Int = field(default='', metadata={'label': 'Size'})
    pivot: bool = field(default=False, metadata={'label': 'Pivot'})


@dataclass
class Tweakable:
    label: str = field(default='', metadata={'label': 'Label'})
    description: str = field(default='', metadata={'label': 'Description'})
    name: str = field(default='variable_name', metadata={'label': 'Variable Name'})
    type: str = field(default='string', metadata={'hidden': True, 'label': 'Data Type', 'options': ['int', 'string', 'float', 'boolean', 'joystick', 'inputaction']})


@dataclass
class IntTweakable(Tweakable):
    initial_value: int = field(default=0, metadata={'label': 'Initial Value'})
    maximum: int = field(default=10, metadata={'label': 'Maximum'})
    minimum: int = field(default=0, metadata={'label': 'Minimum'})


@dataclass
class StringTweakable(Tweakable):
    initial_value: str = field(default='', metadata={'label': 'Initial Value'})
    multiline: bool = field(default=False, metadata={'label': 'Multiple Lines'})


@dataclass
class BooleanTweakable(Tweakable):
    initial_value: bool = field(default=False, metadata={'label': 'Initial Value'})


@dataclass
class FloatTweakable(Tweakable):
    initial_value: float = field(default=0.0, metadata={'label': 'Initial Value'})
    maximum: float = field(default=1.0, metadata={'label': 'Maximum'})
    minimum: float = field(default=0.0, metadata={'label': 'Minimum'})


@dataclass
class JoystickTweakable(Tweakable):
    pass


@dataclass
class InputActionTweakable(Tweakable):
    pass


class HiddenField:
    def __init__(self, type_: Type):
        self.type = type_

    def __name__(self):
        return self.type.__name__

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
    script: str = field(default='', metadata={'label': 'Script', 'hidden': True})
    int_tweakables: List[IntTweakable] = field(default_factory=list, metadata={'hidden': True})
    string_tweakables: List[StringTweakable] = field(default_factory=list, metadata={'hidden': True})
    joystick_tweakables: List[JoystickTweakable] = field(default_factory=list, metadata={'hidden': True})
    inputaction_tweakables: List[InputActionTweakable] = field(default_factory=list, metadata={'hidden': True})
    float_tweakables: List[FloatTweakable] = field(default_factory=list, metadata={'hidden': True})
    boolean_tweakables: List[BooleanTweakable] = field(default_factory=list, metadata={'hidden': True})
    attachments: List[Attachment] = field(default_factory=list, metadata={'hidden': True})


@dataclass
class Mod:
    name: str = field(default='New Mod', metadata={'label': 'Name', 'hidden': True})
    description: str = field(default='', metadata={'label': 'Description'})
    parts: List[Part] = field(default_factory=list, metadata={'hidden': True})