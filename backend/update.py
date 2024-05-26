import os
import shutil
import subprocess
import threading
import zipfile
import eel
import requests
import helpers.github as github
import helpers.updater as updater
from backend.appdata import BEPINEX_VERSION

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

        res = requests.get(github.get_download_url(github.Repos.GEARLIB, 'latest'), stream=True)
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
def update():
    def update():
        for status in updater.download_latest_gearthon():
            progress['editor'] = status

        eel.close_window()
        subprocess.Popen(updater.APP_NAME)

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
