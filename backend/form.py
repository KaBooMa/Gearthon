from dataclasses import fields
import importlib
import eel

#### API ####
@eel.expose
def get_form(class_name):
    module = importlib.import_module(f'classes.{class_name}')

    field_data = []
    for field in fields(getattr(module, class_name)):
        field_data.append({
            'name': field.name,
            'type': field.type.__name__,
            'metadata': dict(field.metadata)
        })

    return field_data