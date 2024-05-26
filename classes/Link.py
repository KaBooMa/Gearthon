from dataclasses import dataclass, field

from classes.Vector3 import Vector3


@dataclass
class Link:
    name: str = field(default='', metadata={'label': 'Name'})
    link_type_name: str = field(default='', metadata={'label': 'Link Type Name (Power, Data, Pulley for native types)'})
    # 'options': [
    #     'Power',
    #     'Data',
    #     'Pulley'
    # ]})
    position: Vector3 = field(default='', metadata={'label': 'Position'})