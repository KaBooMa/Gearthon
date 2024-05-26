from dataclasses import dataclass, field
from typing import List

from classes.Vector3 import Vector3
from classes.Vector3Int import Vector3Int


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
                # 'is_part_pairing_limited'
            ],
            'multiselect': True
        })
    position: Vector3 = field(default='', metadata={'label': 'Position'})
    orientation: Vector3 = field(default='', metadata={'label': 'Orientation'})
    size: Vector3Int = field(default='', metadata={'label': 'Size'})
    pivot: bool = field(default=False, metadata={'label': 'Pivot'})