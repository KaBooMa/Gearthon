import os
import eel

from classes.Part import Part

def clear_selected():
    # Clear all selected
    from backend.link_type import clear_selected_link_type
    clear_selected_link_type()
    from backend.part import clear_selected_part
    clear_selected_part()
    from backend.material import clear_selected_material
    clear_selected_material()
    

#### API ####
@eel.expose
def write_data(path, file, data):
    if not os.path.exists(path):
        os.mkdir(path)
        
    open(f'{path}/{file}', 'w').write(data)


@eel.expose
def load_data(path, file):
    file_path = f'{path}/{file}'
    if not os.path.exists(path) or not os.path.exists():
        return
        
    obj_data = open(file_path).read()
    return obj_data