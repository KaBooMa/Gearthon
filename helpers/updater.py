import requests, shutil, os, time
from zipfile import ZipFile
import helpers.github as github

INTERNALS_NAME = '_internal'
APP_NAME = 'editor.exe'
APP_PATH = '.'

## Check for old exe from being updated
def verify_cleanup():
    time.sleep(1)
    OLD_APP_PATH = f'{APP_PATH}/{APP_NAME}.old'
    if os.path.exists(OLD_APP_PATH):
        os.remove(OLD_APP_PATH)
        
    OLD_INTERNAL_PATH = f'{APP_PATH}/{INTERNALS_NAME}.old'
    if os.path.exists(OLD_INTERNAL_PATH):
        shutil.rmtree(OLD_INTERNAL_PATH)
        

def download_latest_gearthon():
    res = requests.get(f'{github.get_download_url(github.Repos.GEARTHON, "latest")}/Gearthon.zip', stream=True)
    download_size = int(res.headers.get('Content-Length'))
    
    total_downloaded = 0
    with open('gearthon.zip', 'wb') as f:
        for data in res.iter_content(1024):
            total_downloaded += len(data)
            status = round(total_downloaded / download_size * 100, 2)
            f.write(data)
            yield status

    app_path = f'{APP_PATH}/{APP_NAME}'
    shutil.move(app_path, f'{app_path}.old')
    shutil.move(f'{APP_PATH}/{INTERNALS_NAME}', f'{APP_PATH}/{INTERNALS_NAME}.old')

    with ZipFile('gearthon.zip', 'r') as zip:
        zip.extractall()

    os.remove('gearthon.zip')