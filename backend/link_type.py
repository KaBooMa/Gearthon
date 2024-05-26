from dataclasses import asdict
import random
import eel

from classes.LinkType import LinkType

selected_link_type: LinkType = None

def clear_selected_link_type():
    global selected_link_type
    selected_link_type = None

#### API ####
@eel.expose
def select_link_type(uid):
    from backend.mod import mod
    global selected_link_type

    for link_type in mod.link_types:
        if link_type.uid == uid:
            from backend.editor import clear_selected
            clear_selected()

            selected_link_type = link_type
            break


@eel.expose
def update_link_type(kwargs):
    from backend.mod import mod
    if not mod:
        return None
    
    global selected_link_type
    for key, value in kwargs.items():
        setattr(selected_link_type, key, value)


@eel.expose
def get_link_type():
    if not selected_link_type:
        return None
    
    return asdict(selected_link_type)


@eel.expose
def create_link_type():
    from backend.mod import mod
    if not mod:
        return None
    
    mod.link_types.append(LinkType(uid=random.randint(1, 10**16)))


@eel.expose
def delete_link_type(uid):
    from backend.mod import mod
    if not mod:
        return None
    
    for i, link_type in enumerate(mod.link_types):
        if link_type.uid == uid:
            ## TODO: Add icons for link types; Code already here for ya buddy ;)
            # Delete texture if there is one
            # model_path = current_texture_file()
            # if os.path.exists(model_path):
            #     os.remove(model_path)
            
            mod.link_types.pop(i)
            global selected_link_type
            if selected_link_type == link_type:
                selected_link_type = None
                
            break