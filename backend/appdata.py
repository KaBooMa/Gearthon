from dataclasses import dataclass, field, asdict
from dacite import from_dict
from tkinter import filedialog, messagebox
import eel
import os
import json
import helpers.github as github
import requests

BEPINEX_VERSION = 'https://builds.bepinex.dev/projects/bepinex_be/690/BepInEx-Unity.IL2CPP-win-x86-6.0.0-be.690%2B36d130f.zip'
APPDATA_FILE = 'data.json'
CURRENT_VERSION = '1.0.4'

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
    gearlib_version: str = field(default='0.0.0')
    bepinex_version: str = field(default='0.0.0')
    setup: bool = False

    def is_gearlib_updated(self):
        res = requests.get(github.get_api_url(github.Repos.GEARLIB, 'latest'))
        latest_version = res.json()['tag_name']
        return self._is_update_latest(self.gearlib_version, latest_version)


    def is_gearthon_updated(self):
        res = requests.get(github.get_api_url(github.Repos.GEARTHON, 'latest'))
        latest_version = res.json()['tag_name']
        return self._is_update_latest(self.version, latest_version)


    def is_bepinex_updated(self):
        return self.bepinex_version == BEPINEX_VERSION
    

    def _is_update_latest(self, current_version, latest_version):
        v1 = current_version.split('.')
        v2 = latest_version.split('.')

        for i, v in enumerate(v2):
            if v1[i] > v:
                break
            
            if len(v2)-1 >= i and v > v1[i]:
                return False

        return True

    def bepinex_folder(self):
        return f'{self.gearblocks_path}/BepInEx/plugins'


    def gearlib_folder(self):
        return f'{self.bepinex_folder()}/GearLib'


    def gearthon_folder(self):
        return f'{self.bepinex_folder()}/Gearthon'


    def mods_folder(self):
        return f'{self.gearthon_folder()}/mods'


    def save(self):
        data = json.dumps(asdict(self))
        with open(APPDATA_FILE, 'w') as f:
            f.write(data)


### API ####
appdata: AppData = None

@eel.expose
def get_appdata():
    global appdata

    # Check if we've already loaded appdata
    if not appdata:
        appdata = load_appdata()

    return asdict(appdata)


@eel.expose
def save_appdata():
    # Ensure we have a appdata currently
    if not appdata:
        return

    appdata.save()


@eel.expose
def update_appdata(kwargs):
    global appdata
    if not appdata:
        return None
    
    for key, value in kwargs.items():
        setattr(appdata, key, value)

    save_appdata()


@eel.expose
def update_gearblocks_folder():
    global appdata
    path = filedialog.askdirectory()
    if os.path.exists(path) and os.path.exists(f'{path}/GearBlocks.exe'):
        appdata.gearblocks_path = path
        appdata.save()
    else:
        messagebox.showinfo('Invalid Folder', 'No GearBlocks.exe found. Ensure you selected the right folder!')


@eel.expose
def bepinex_exists():
    return os.path.exists(f'{appdata.gearblocks_path}/BepInEx')


@eel.expose
def gearlib_exists():
    return os.path.exists(f'{appdata.gearblocks_path}/BepInEx/plugins/GearLib')


@eel.expose
def gearthon_exists():
    return os.path.exists(f'{appdata.gearblocks_path}/BepInEx/plugins/Gearthon')
