import subprocess
import requests
import json
import autoDownload
import re
from lxml import etree
import cloudscraper

curseforge_new_list = []
curseforge_old_list = []

def load_json(minecraft_version):
    scraper = cloudscraper.create_scraper()
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
            item["homepage"] = homepage.replace("https://minecraft.curseforge.com/projects/", "https://www.curseforge.com/minecraft/mc-mods/")
        if sources:
            item["sources"] = sources.replace("https://minecraft.curseforge.com/projects/", "https://www.curseforge.com/minecraft/mc-mods/")

    # 遍历字典并将所有的homepage和sources添加到列表中
    curseforge_list = []
    for item in curseforge_old + curseforge_new:
        homepage = item.get("homepage")
        if homepage:
            curseforge_list.append(homepage)
        sources = item.get("sources")
        if sources:
            curseforge_list.append(sources)

    # 打印所有的homepage和sources
    for mod_url in curseforge_list:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = scraper.get(mod_url, headers=headers)
        if response.status_code == 200:
            html = response.content
            tree = etree.HTML(html)
            version_elements = tree.xpath('//*[@id="project-versions"]/li/a')
            versions = [elem.text for elem in version_elements]
            for i in versions:
                if i == minecraft_version:
                    # https://www.curseforge.com/minecraft/mc-mods/autofish/files?version=1.19.4
                    url = f"https://www.curseforge.com/minecraft/mc-mods/autofish/files?version={i}"
                    result = scraper.get(url, headers=headers).text
                    html = response.content
                    tree = etree.HTML(html)
                    font_element = tree.xpath('//*[@id="contextMenu"]')[0]
                    text = font_element.text
                    print(text)

        else:
            print(f"Error getting HTML for {mod_url}: {response.status_code}")   

version = input('请输入你的版本号:')
load_json(version)