from dataclasses import asdict
import os
import random
import eel

from backend.mod import current_mod_path
from classes.Part import Part

selected_part: Part = None
MODELS_FOLDER = 'models'

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


def clear_selected_part():
    global selected_part
    selected_part = None

#### API ####
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
def select_part(part_uid):
    global selected_part
    from backend.mod import mod
    for part in mod.parts:
        if part.uid == part_uid:
            from backend.editor import clear_selected
            clear_selected()

            selected_part = part
            break


@eel.expose
def update_part(kwargs):
    from backend.mod import mod
    if not mod:
        return None
    
    global selected_part
    for key, value in kwargs.items():
        setattr(selected_part, key, value)


@eel.expose
def get_selected_part():
    from backend.mod import mod
    if not mod or not selected_part:
        return None 
    
    return asdict(selected_part)


@eel.expose
def create_part():
    from backend.mod import mod
    if not mod:
        return None
    
    mod.parts.append(Part(random.randint(1, 10**16)))


@eel.expose
def delete_part(part_uid):
    from backend.mod import mod
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