from dataclasses import dataclass, field


@dataclass
class Tweakable:
    label: str = field(default='', metadata={'label': 'Label'})
    description: str = field(default='', metadata={'label': 'Description'})
    name: str = field(default='variable_name', metadata={'label': 'Variable Name'})
    type: str = field(default='string', metadata={'hidden': True, 'label': 'Data Type', 'options': ['int', 'string', 'float', 'boolean', 'joystick', 'inputaction']})