from dataclasses import asdict
import json
import os
from pathlib import Path
import shutil
from tkinter import filedialog
import zipfile
from dacite import from_dict
import eel
from classes.Mod import Mod

MOD_FILE_NAME = 'mod.json'
mod: Mod = None

def current_mod_path():
    if not mod:
        return None
    
    from backend.appdata import appdata
    mod_folder = f'{appdata.mods_folder()}/{mod.name}'
    if not os.path.exists(appdata.mods_folder()):
        os.mkdir(appdata.mods_folder())

    if not os.path.exists(mod_folder):
        os.mkdir(mod_folder)
    
    return mod_folder


def current_mod_file():
    if not mod:
        return None
    
    return f'{current_mod_path()}/{MOD_FILE_NAME}'


#### API ####
@eel.expose
def create_mod(name):
    global mod
    mod = Mod(name)

    from backend.editor import clear_selected
    clear_selected()
    

@eel.expose
def get_mod():
    if not mod:
        return None
    
    return asdict(mod)


@eel.expose
def get_mods():
    from backend.appdata import appdata
    if not os.path.exists(appdata.mods_folder()):
        return None
    
    return os.listdir(appdata.mods_folder())


@eel.expose
def save_mod():
    if not mod:
        return
    
    data = asdict(mod)

    from backend.appdata import appdata
    if not os.path.exists(appdata.mods_folder()):
        os.mkdir(appdata.mods_folder())

    mod_path = current_mod_path()
    if not os.path.exists(mod_path):
        os.mkdir(mod_path)
    
    json_path = current_mod_file()
    with open(json_path, 'w') as f:
        f.write(json.dumps(data))


@eel.expose
def rename_mod(name, new_name, new_description):
    from backend.appdata import appdata
    mod_path = Path(f'{appdata.mods_folder()}/{name}')
    new_mod_path = Path(f'{appdata.mods_folder()}/{new_name}')
    mod_json_path = Path(f'{appdata.mods_folder()}/{name}/mod.json')

    with open(mod_json_path, 'r') as mod_json:
        mod_data = json.load(mod_json)

    mod_data['name'] = new_name
    mod_data['description'] = new_description

    with open(mod_json_path, 'w') as mod_json:
        json.dump(mod_data, mod_json, indent=4)
    
    os.mkdir(new_mod_path)

    for item in os.listdir(mod_path):
        shutil.move(os.path.join(mod_path, item), new_mod_path)

    shutil.rmtree(mod_path)

    from backend.editor import clear_selected
    clear_selected()

@eel.expose
def import_mod():
    path = filedialog.askopenfilename(defaultextension='.gearthon', filetypes=[('Gearthon Mods', '*.gearthon')])

    with zipfile.ZipFile(path) as zip:
        first_dir = zip.filelist[0].filename
        from backend.appdata import appdata
        mod_path = f'{appdata.mods_folder}/{first_dir}'
        if os.path.exists(mod_path):
            os.remove(mod_path)

        zip.extractall(appdata.mods_folder())


@eel.expose
def export_mod(name):
    path = filedialog.askdirectory()
    from backend.appdata import appdata
    mod_path = Path(f'{appdata.mods_folder()}/{name}')
    shutil.make_archive(f'{path}/{name}.gearthon', 'zip', root_dir=mod_path.parent, base_dir=f'./{name}')
    shutil.move(f'{path}/{name}.gearthon.zip', f'{path}/{name}.gearthon')


@eel.expose
def load_mod(name):
    from backend.appdata import appdata
    mod_path = f'{appdata.mods_folder()}/{name}'
    if not os.path.exists(mod_path):
        return
    
    raw_data = open(f'{mod_path}/{MOD_FILE_NAME}').read()
    data = json.loads(raw_data)
    
    global mod, selected_part
    mod = from_dict(Mod, data)
    selected_part = None


@eel.expose
def delete_mod(name):
    from backend.appdata import appdata
    mod_path = f'{appdata.mods_folder()}/{name}'
    if not os.path.exists(mod_path):
        return
    
    global mod
    if mod and mod.name == name:
        mod = None
    
    shutil.rmtree(mod_path)