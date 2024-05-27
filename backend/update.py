import os
import shutil
import subprocess
import threading
import time
import zipfile
import eel
import requests

import helpers.github as github
from backend.appdata import BEPINEX_VERSION

INTERNALS_NAME = '_internal'
APP_NAME = ['editor.exe', 'Gearthon.exe']
APP_PATH = '.'

def update_cleanup():
    for name in APP_NAME:
        OLD_APP_PATH = f'{APP_PATH}/{name}.old'
        if os.path.exists(OLD_APP_PATH):
            os.remove(OLD_APP_PATH)
        
    OLD_INTERNAL_PATH = f'{APP_PATH}/{INTERNALS_NAME}.old'
    if os.path.exists(OLD_INTERNAL_PATH):
        shutil.rmtree(OLD_INTERNAL_PATH)

#### API ####
progress = {}

@eel.expose
def update_bepinex():
    def update():
        from backend.appdata import appdata
        global progress
        progress['bepinex'] = 0

        res = requests.get(BEPINEX_VERSION, stream=True)
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

        # Update BepInEx version in appdata
        appdata.bepinex_version = BEPINEX_VERSION
        appdata.save()

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def update_gearlib():
    def update():
        from backend.appdata import appdata
        global progress
        progress['gearlib'] = 0
        res = requests.get(f'{github.get_download_url(github.Repos.GEARLIB, "latest")}/GearLib.zip', stream=True)
        version = github.get_tag(github.Repos.GEARLIB, 'latest')
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

        # Update GearLib version in appdata
        appdata.gearlib_version = version
        appdata.save()

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def update_gearthon():
    def update():
        res = requests.get(f'{github.get_download_url(github.Repos.GEARTHON, "latest")}/Gearthon.zip', stream=True)
        download_size = int(res.headers.get('Content-Length'))
        
        total_downloaded = 0
        with open('gearthon.zip', 'wb') as f:
            for data in res.iter_content(1024):
                total_downloaded += len(data)
                status = round(total_downloaded / download_size * 100, 2)
                f.write(data)
                progress['gearthon'] = status

        for name in APP_NAME:
            app_path = f'{APP_PATH}/{name}'
            if os.path.exists(app_path):
                shutil.move(app_path, f'{app_path}.old')

        internals_path = f'{APP_PATH}/{INTERNALS_NAME}'
        if os.path.exists(internals_path):
            shutil.move(internals_path, f'{internals_path}.old')

        with zipfile.ZipFile('gearthon.zip', 'r') as zip:
            zip.extractall()

        os.remove('gearthon.zip')

        eel.close_window()
        subprocess.Popen(APP_NAME)

    thread = threading.Thread(target=update)
    thread.start()


@eel.expose
def is_gearlib_updated():
    from backend.appdata import appdata
    return appdata.is_gearlib_updated()


@eel.expose
def is_gearthon_updated():
    from backend.appdata import appdata
    return appdata.is_gearthon_updated()


@eel.expose
def is_bepinex_updated():
    from backend.appdata import appdata
    return appdata.is_bepinex_updated()


@eel.expose
def get_progress(key):
    if key in progress:
        return progress[key]
    else:
        return 0
