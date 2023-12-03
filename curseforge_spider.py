import json
import requests
from lxml import etree
import autoDownload
import setconfig
import os
import shutil

import setconfig

curseforge_new_list = []
curseforge_old_list = []
curseforge_list = []


def load_json(): \
        # 读取curseforge_old.json文件
    with open('curseforge_old.json', 'r') as f:
        curseforge_old = json.load(f)

    # 读取curseforge_new.json文件
    with open('curseforge_new.json', 'r') as f:
        curseforge_new = json.load(f)

    # 替换URL
    for item in curseforge_old + curseforge_new:
        homepage = item.get("homepage")
        sources = item.get("sources")
        if homepage:
            item["homepage"] = homepage.replace("https://minecraft.curseforge.com/projects/",
                                                "https://www.curseforge.com/minecraft/mc-mods/")
        if sources:
            item["sources"] = sources.replace("https://minecraft.curseforge.com/projects/",
                                              "https://www.curseforge.com/minecraft/mc-mods/")

    # 遍历字典并将所有的homepage和sources添加到列表中
    curseforge_list = []
    for item in curseforge_old + curseforge_new:
        homepage = item.get("homepage")
        if homepage:
            curseforge_list.append(homepage)
        sources = item.get("sources")
        if sources:
            curseforge_list.append(sources)

    def get_information(version, version_type):
        global curseforge_list
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
        for mod in curseforge_list:
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
                        mod_dir = os.path.join(temp_dir, modname)
                        downloader = autoDownload.AutoDownload(link, mod_dir)
                        downloader.start()
                else:
                    print(f"Error getting HTML for {homepage}: {response.status_code}")
            elif sources:
                print(f"No homepage found for {modname}, using sources instead: {sources}")
            else:
                print(f"No homepage or sources found for {modname}")
        print('Download success!')
        minecraft_mods_dir = setconfig.get_config("mods_path")
        for mod in curseforge_list:
            modname = mod.get('modname')
            if modname:
                backup_folder_path = os.path.join(os.getcwd(), "backup")
                if not os.path.exists(backup_folder_path):
                    os.mkdir(backup_folder_path)
                for root, dirs, files in os.walk(os.path.join(minecraft_mods_dir, "")):
                    for file in files:
                        # 如果文件名与指定的文件名相同，则删除该文件
                        if file == modname:
                            file_path = os.path.join(root, file)
                            backup_file_path = os.path.join(backup_folder_path, file)
                            shutil.move(file_path, backup_file_path)
                            print(f"Moved file '{file}' to backup folder.")
                print('Old jars moved successfully!')
        # 移动更新后的mod
        src_folder_path = os.path.join(os.getcwd(), "TEMP_jar")
        dst_folder_path = os.path.join(minecraft_mods_dir, "")

        # 遍历源文件夹中的所有文件和文件夹
        for root, dirs, files in os.walk(src_folder_path):
            for file in files:
                # 构建源文件路径和目标文件路径
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(dst_folder_path, file)

                # 移动文件到目标文件夹中
                shutil.move(src_file_path, dst_file_path)
                print(f"Moved file '{file}' to destination folder.")
        print("New jars moved successfully!")

        print("File move completed.")

    def run(version, version_type):
        load_json()
        get_information(version, version_type)
