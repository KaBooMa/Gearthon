import importlib
import inspect
import pkgutil
import os

# Automatically import all submodules
package_dir = os.path.dirname(__file__)
for (_, module_name, _) in pkgutil.iter_modules([package_dir]):
    module = importlib.import_module(f'{__name__}.{module_name}')

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            globals().update({name: obj})