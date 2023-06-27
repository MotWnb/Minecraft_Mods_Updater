import json
import requests
from lxml import etree
import autoDownload
import setconfig
import os
import shutil


modrinth_list = []



def load_json():
    global modrinth_list
    with open('modrinth.json') as f:
        data = json.load(f)

    for mod in data:
        mod_dict = {}
        homepage = mod.get('homepage')
        sources = mod.get('sources')
        modname = mod.get('modname')
        if homepage:
            mod_dict['homepage'] = homepage
        if sources:
            mod_dict['sources'] = sources
        if modname:
            mod_dict['modname'] = modname
        modrinth_list.append(mod_dict)


def get_information(version, version_type):
    global modrinth_list
    temp_dir = os.path.join(os.getcwd(), "TEMP_jar")
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
        print(f"Created temp directory: {temp_dir}")
    else:
        shutil.rmtree(temp_dir)
        print(f"Deleted temp directory: {temp_dir}")
        os.mkdir(temp_dir)
        print(f"Created temp directory: {temp_dir}")
    os.chmod(temp_dir, 0o777)
    for mod in modrinth_list:
        homepage = mod.get('homepage')
        sources = mod.get('sources')
        modname = mod.get('modname')
        if homepage:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            # https://modrinth.com/mod/mixintrace/versions?l=fabric&g=1.19.4
            url = homepage + f"/versions?l={version_type}&g={version}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html = response.content
                tree = etree.HTML(html)
                download_link = tree.xpath("//*[@id='all-versions']/div[2]/a[1]/@href")
                if download_link:
                    link = download_link[0]
                    print(link)
                    # autoDownload.AutoDownload(URL,file,key=value...).start()
                    filename = setconfig.get_config("mods_path")
                    mod_dir = os.path.join(temp_dir, modname)
                    downloader = autoDownload.AutoDownload(link, mod_dir)
                    downloader.start()
            else:
                print(f"Error getting HTML for {homepage}: {response.status_code}")
        elif sources:
            print(f"No homepage found for {modname}, using sources instead: {sources}")
        else:
            print(f"No homepage or sources found for {modname}")


def run(version, version_type):
    print("getting!!!!!!")
    load_json()
    get_information(version, version_type)

# run("1.19.4", "fabric")