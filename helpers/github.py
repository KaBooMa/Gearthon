import requests

class Repos:
    GEARLIB: str = 'KaBooMa/GearLib'
    GEARTHON: str = 'KaBooMa/Gearthon'
    

def get_api_url(repo, release):
    return f'https://api.github.com/repos/{repo}/releases/{release}'


def get_download_url(repo, release):
    return f'https://github.com/{repo}/releases/{release}/download'


def get_tag(repo, release):
    res = requests.get(get_api_url(repo, release))
    return res.json()['tag_name']