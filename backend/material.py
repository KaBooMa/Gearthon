import base64
from dataclasses import asdict
import os
from pathlib import Path
import random
import shutil
from tkinter import filedialog
import eel

from backend.mod import current_mod_path
from classes.Material import Material

selected_material: Material = None
TEXTURES_FOLDER = 'textures'

def current_texture_path():
    if not selected_material:
        return
    
    mod_folder = current_mod_path()
    model_path = f'{mod_folder}/{TEXTURES_FOLDER}'
    if not os.path.exists(model_path):
        os.mkdir(model_path)
    
    return model_path


def current_texture_file():
    if not selected_material:
        return
    
    return f'{current_texture_path()}/{selected_material.uid}.{selected_material.file_type}'


def clear_selected_material():
    global selected_material
    selected_material = None

#### API ####
@eel.expose
def upload_material_texture():
    path = filedialog.askopenfilename()
    if not path:
        return
    
    path = Path(path)
    global selected_material
    selected_material.file_type = path.suffix[1:]
    shutil.copy(path, current_texture_file())


@eel.expose
def get_material_texture():
    data = open(current_texture_file(), 'rb').read()
    image = base64.b64encode(data).decode('utf-8')
    return f'data:image/{selected_material.file_type};base64,{image}'



@eel.expose
def select_material(uid):
    from backend.mod import mod
    global selected_material

    for material in mod.materials:
        if material.uid == uid:
            from backend.editor import clear_selected
            clear_selected()

            selected_material = material
            break


@eel.expose
def update_material(kwargs):
    from backend.mod import mod
    if not mod:
        return None
    
    global selected_material
    for key, value in kwargs.items():
        setattr(selected_material, key, value)


@eel.expose
def get_material():
    if not selected_material:
        return None
    
    return asdict(selected_material)


@eel.expose
def create_material():
    from backend.mod import mod
    if not mod:
        return None
    
    mod.materials.append(Material(uid=random.randint(1, 10**16)))


@eel.expose
def delete_material(uid):
    from backend.mod import mod
    if not mod:
        return None
    
    for i, material in enumerate(mod.materials):
        if material.uid == uid:
            # Delete texture if there is one
            model_path = current_texture_file()
            if os.path.exists(model_path):
                os.remove(model_path)
            
            mod.materials.pop(i)
            global selected_material
            if selected_material == material:
                selected_material = None
                
            break