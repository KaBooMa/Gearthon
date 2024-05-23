import requests, shutil, os, time
from zipfile import ZipFile
from appdata import CURRENT_VERSION

GITHUB_API_URL = 'https://api.github.com/repos/KaBooMa/Gearthon/releases/latest'
GITHUB_DOWNLOAD_URL = 'https://github.com/KaBooMa/Gearthon/releases/latest/download'

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


def check_for_update():
    res = requests.get(GITHUB_API_URL)
    latest = res.json()
    latest_version: str = latest['tag_name']

    v1 = CURRENT_VERSION.split('.')
    v2 = latest_version.split('.')

    for i, v in enumerate(v2):
        if v1[i] > v:
            break
        
        if len(v2)-1 >= i and v > v1[i]:
            return True

    return False
        

def download_latest_gearthon():
    res = requests.get(f'{GITHUB_DOWNLOAD_URL}/Gearthon.zip', stream=True)
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