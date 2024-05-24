### This fix is applied to allow pyinstaller!! ###
import sys, os, io

if not os.path.exists('../README.md'):
    logfile = io.StringIO()
    sys.stdout = logfile
    sys.stderr = logfile
    DEBUG = False
else:
    DEBUG = True
##################################################

import os, shutil, eel, json, random, requests, zipfile, updater, subprocess, threading
from dacite import from_dict
from classes import *
from dataclasses import asdict, fields
from appdata import AppData, load_appdata
from tkinter import filedialog, messagebox
from pathlib import Path

eel.init('web', allowed_extensions=['.html'])

#### APP API ####
appdata: AppData = None
BEPINEX_LINK = 'https://builds.bepinex.dev/projects/bepinex_be/690/BepInEx-Unity.IL2CPP-win-x86-6.0.0-be.690%2B36d130f.zip'
GEARLIB_LINK = 'https://github.com/KaBooMa/GearLib/releases/latest/download/GearLib.zip'

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


#### UPDATE API ####
progress = {}

@eel.expose
def update_bepinex():
    def update():
        global progress
        progress['bepinex'] = 0

        res = requests.get(BEPINEX_LINK, stream=True)
        download_size = int(res.headers.get('Content-Length'))

        total_downloaded = 0
        with open('bepinex.zip', 'wb') as f:
            for data in res.iter_content(1024):
                total_downloaded += len(data)
                status = round(total_downloaded / download_size * 100, 2)
                f.write(data)
                progress['bepinex'] = status

        with zipfile.ZipFile('bepinex.zip', 'r') as zip:
            zip.extractall(appdata.gearblocks_path)

        os.remove('bepinex.zip')

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def update_gearlib():
    def update():
        global progress
        progress['gearlib'] = 0

        res = requests.get(GEARLIB_LINK, stream=True)
        download_size = int(res.headers.get('Content-Length'))
        
        total_downloaded = 0
        with open('gearlib.zip', 'wb') as f:
            for data in res.iter_content(1024):
                total_downloaded += len(data)
                status = round(total_downloaded / download_size * 100, 2)
                f.write(data)
                progress['gearlib'] = status

        plugin_path = f'{appdata.gearblocks_path}/BepInEx/plugins'
        if os.path.exists(f'{plugin_path}/GearLib'):
            shutil.rmtree(f'{plugin_path}/GearLib')

        with zipfile.ZipFile('gearlib.zip', 'r') as zip:
            zip.extractall(f'{appdata.gearblocks_path}/BepInEx/plugins')

        os.remove('gearlib.zip')

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def update():
    def update():
        for status in updater.download_latest_gearthon():
            progress['editor'] = status

        eel.close_window()
        subprocess.Popen(updater.APP_NAME)

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def check_for_update():
    return updater.check_for_update()


@eel.expose
def get_progress(key):
    if key in progress:
        return progress[key]
    else:
        return 0


#### MOD API ####
MODELS_FOLDER = 'models'
MOD_FILE_NAME = 'mod.json'
mod: Mod = None

def current_mod_path():
    if not mod:
        return None
    
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


@eel.expose
def create_mod(name):
    global mod
    mod = Mod(name)

    global selected_part
    if selected_part:
        selected_part = None
    

@eel.expose
def get_mod():
    if not mod:
        return None
    
    return asdict(mod)


@eel.expose
def get_mods():
    if not os.path.exists(appdata.mods_folder()):
        return None
    
    return os.listdir(appdata.mods_folder())


@eel.expose
def save_mod():
    if not mod:
        return
    
    data = asdict(mod)

    if not os.path.exists(appdata.mods_folder()):
        os.mkdir(appdata.mods_folder())

    mod_path = current_mod_path()
    if not os.path.exists(mod_path):
        os.mkdir(mod_path)
    
    json_path = current_mod_file()
    with open(json_path, 'w') as f:
        f.write(json.dumps(data))


@eel.expose
def import_mod():
    path = filedialog.askopenfilename(defaultextension='.gearthon', filetypes=[('Gearthon Mods', '*.gearthon')])

    with zipfile.ZipFile(path) as zip:
        first_dir = zip.filelist[0].filename
        mod_path = f'{appdata.mods_folder}/{first_dir}'
        if os.path.exists(mod_path):
            os.remove(mod_path)

        zip.extractall(appdata.mods_folder())


@eel.expose
def export_mod(name):
    path = filedialog.askdirectory()
    mod_path = Path(f'{appdata.mods_folder()}/{name}')
    shutil.make_archive(f'{path}/{name}.gearthon', 'zip', root_dir=mod_path.parent, base_dir=f'./{name}')
    shutil.move(f'{path}/{name}.gearthon.zip', f'{path}/{name}.gearthon')


@eel.expose
def load_mod(name):
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
    mod_path = f'{appdata.mods_folder()}/{name}'
    if not os.path.exists(mod_path):
        return
    
    global mod
    if mod and mod.name == name:
        mod = None
    
    shutil.rmtree(mod_path)

    


#### PART API ####
selected_part: Part = None

def current_model_path():
    if not selected_part:
        return
    
    mod_folder = current_mod_path()
    model_path = f'{mod_folder}/{MODELS_FOLDER}'
    if not os.path.exists(model_path):
        os.mkdir(model_path)
    
    return model_path


def current_model_file():
    if not selected_part:
        return
    
    return f'{current_model_path()}/{selected_part.uid}.obj'


@eel.expose
def select_part(part_uid):
    global selected_part
    for part in mod.parts:
        if part.uid == part_uid:
            selected_part = part
            break


@eel.expose
def update_selected_part(kwargs):
    if not mod:
        return None
    
    global selected_part
    for key, value in kwargs.items():
        setattr(selected_part, key, value)


@eel.expose
def write_part_obj(obj_data):
    if not selected_part:
        return
    
    model_folder = current_model_path()
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)
        
    model_path = current_model_file()
    open(model_path, 'w').write(obj_data)


@eel.expose
def load_part_obj():
    if not selected_part:
        return
    
    model_folder = current_model_path()
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)
        
    model_path = current_model_file()
    if not os.path.exists(model_path):
        return
    
    obj_data = open(model_path).read()
    return obj_data


@eel.expose
def get_selected_part():
    if not mod or not selected_part:
        return None 
    
    return asdict(selected_part)


@eel.expose
def create_part():
    if not mod:
        return None
    
    mod.parts.append(Part(random.randint(1, 10**16)))


@eel.expose
def delete_part(part_uid):
    if not mod:
        return None
    
    for i, part in enumerate(mod.parts):
        part: Part = mod.parts[i]
        if part.uid == part_uid:
            # Delete model if there is one
            model_path = current_model_file()
            if os.path.exists(model_path):
                os.remove(model_path)
            
            mod.parts.pop(i)
            global selected_part
            if selected_part == part:
                selected_part = None
                
            break


#### FORM API ####
@eel.expose
def get_form(class_name):
    field_data = []
    for field in fields(globals()[class_name]):
        field_data.append({
            'name': field.name,
            'type': field.type.__name__,
            'metadata': dict(field.metadata)
        })

    return field_data

# Run any cleanups or whatever
updater.verify_cleanup()

OLD_GEARTHON_DLL_PATH = f'{appdata.gearthon_folder()}/Gearthon.dll'
if os.path.exists(OLD_GEARTHON_DLL_PATH):
    os.remove(OLD_GEARTHON_DLL_PATH)


# Start the frontend
eel.start('index.html?page=home', size=(1500, 800))