import requests
import json
import re


def load_json():
    global modrinth
    # 读取modrinth.json文件
    with open('curseforge_old.json', 'r') as f:
        modrinth = json.load(f)

