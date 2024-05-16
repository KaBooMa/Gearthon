from dataclasses import dataclass, field, asdict
from dacite import from_dict
from tkinter import filedialog, messagebox
import os, json

APPDATA_FILE = 'data.json'
CURRENT_VERSION = '1.0.0'

def get_gearblocks_path():
    DEFAULT_PATHS = ['C:/Program Files (x86)/Steam/steamapps/common/GearBlocks']
    
    # Check if gearblocks is in one of the defaults
    for path in DEFAULT_PATHS:
        if os.path.exists(path):
            return path
        
    # Allow user to manually select folder
    messagebox.showinfo('Locate GearBlocks Folder', 'Unable to find GearBlocks folder automatically. Please manually locate your GearBlocks folder. This is typically located in your Steam folder.')
    path = filedialog.askdirectory()
    if os.path.exists(path) and os.path.exists(f'{path}/GearBlocks.exe'):
        return path
    
    raise Exception('Unable to locate GearBlocks folder! Please ensure you selected the correct folder.')


def load_appdata():
    # Create if doesn't exist
    if not os.path.exists(APPDATA_FILE):
        appdata = AppData()
        appdata.save()
    else: # Lets load the existing appdata
        raw_data = open(APPDATA_FILE).read()
        data = json.loads(raw_data)
        appdata = from_dict(AppData, data)

        # Update versioning if running a different build
        if appdata.version != CURRENT_VERSION:
            appdata.version = CURRENT_VERSION
            appdata.save()

    return appdata

@dataclass
class AppData:
    gearblocks_path: str = field(default_factory=get_gearblocks_path)
    theme: str = field(default='default')
    version: str = field(default=CURRENT_VERSION)
    setup: bool = False

    def save(self):
        data = json.dumps(asdict(self))
        with open(APPDATA_FILE, 'w') as f:
            f.write(data)