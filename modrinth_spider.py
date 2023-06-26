import json
import requests
from lxml import etree
import autoDownload
import tempfile


modrinth_list = []

def load_json():
    global modrinth_list
    with open('modrinth.json') as f:
        data = json.load(f)

    for mod in data:
        homepage = mod.get('homepage')
        sources = mod.get('sources')
        dirpath = mod.get('dirpath')
        if homepage:
            modrinth_list.append(homepage)
        if sources:
            modrinth_list.append(sources)
        if dirpath:
            modrinth_list.append(dirpath)


def get_information(version, version_type):
    global modrinth_list
    for url in modrinth_list:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        # https://modrinth.com/mod/mixintrace/versions?l=fabric&g=1.19.4
        url = url + f"/versions?l={version_type}&g={version}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.content
            tree = etree.HTML(html)
            download_link = tree.xpath("//*[@id='all-versions']/div[2]/a[1]/@href")
            if download_link:
                print(download_link[0])
                # autoDownload.AutoDownload(URL,file,key=value...).start()
                downloader = autoDownload.AutoDownload
        else:
            print(f"Error getting HTML for {url}: {response.status_code}")


def run(version, version_type):
    print("getting!!!!!!")
    load_json()
    get_information(version, version_type)
