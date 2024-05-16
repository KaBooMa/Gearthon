import requests, shutil, os
from zipfile import ZipFile
from appdata import CURRENT_VERSION

GITHUB_URL = 'https://api.github.com/repos/KaBooMa/Gearthon/releases/latest'

INTERNALS_NAME = '_internal'
APP_NAME = 'editor.exe'
APP_PATH = '.'

## Check for old exe from being updated
def verify_cleanup():
    OLD_APP_PATH = f'{APP_PATH}/{APP_NAME}.old'
    if os.path.exists(OLD_APP_PATH):
        os.remove(OLD_APP_PATH)
        
    OLD_INTERNAL_PATH = f'{APP_PATH}/{INTERNALS_NAME}.old'
    if os.path.exists(OLD_INTERNAL_PATH):
        shutil.rmtree(OLD_INTERNAL_PATH)


def check_for_update():
    res = requests.get(GITHUB_URL)
    latest = res.json()
    latest_version = latest['tag_name']

    v1 = CURRENT_VERSION.split('.')
    v2 = latest_version.split('.')
    print(CURRENT_VERSION)
    print(latest_version)

    for i, v in enumerate(v2):
        if v1[i] > v:
            break
        
        if len(v2)-1 >= i and v > v1[i]:
            print(v, v2[i])
            print(f'{latest_version} is newer than {CURRENT_VERSION}')
            return True

    return False
        

def download_latest():
    res = requests.get(f'{GITHUB_URL}/Gearthon.zip')
    with open('gearthon.zip', 'wb') as f:
        f.write(res.content)

    app_path = f'{APP_PATH}/{APP_NAME}'
    shutil.move(app_path, f'{app_path}.old')
    shutil.move(f'{APP_PATH}/{INTERNALS_NAME}', f'{APP_PATH}/{INTERNALS_NAME}.old')

    with ZipFile('gearthon.zip', 'r') as zip:
        zip.extractall(APP_PATH)