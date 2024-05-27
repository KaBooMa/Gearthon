### This fix is applied to allow pyinstaller!! ###
import sys, os, io
import time

if not os.path.exists('README.md'):
    logfile = io.StringIO()
    sys.stdout = logfile
    sys.stderr = logfile
    DEBUG = False
else:
    DEBUG = True
##################################################

import eel

# Run any cleanups or whatever
from backend.update import update_cleanup
update_cleanup()

# Clean up old Gearthon.dll way of modding
from backend.appdata import get_appdata
get_appdata()
from backend.appdata import appdata
OLD_GEARTHON_DLL_PATH = f'{appdata.gearthon_folder()}/Gearthon.dll'
if os.path.exists(OLD_GEARTHON_DLL_PATH):
    os.remove(OLD_GEARTHON_DLL_PATH)
    

#########################
#### Run Application ####
#########################

eel.init('web', allowed_extensions=['.html'])

# Load all endpoints (the __init__.py loads all submodules)
import backend

# Start the frontend
eel.start('index.html?page=home', size=(1500, 800))