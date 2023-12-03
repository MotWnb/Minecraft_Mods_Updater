import fnmatch
import os
import json
import tempfile
import zipfile
import modrinth_spider

curseforge_new = []
curseforge_old = []
modrinth = []


def process_fabric_mod_json(file_path, modname):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.loads(f.read())
        except json.JSONDecodeError as e:
            print(f"JSON解析错误:{e}")
            return

    homepage = data.get("contact", {}).get("homepage")
    sources = data.get("contact", {}).get("sources")

    if homepage is not None and "modrinth.com" in homepage:
        modrinth.append({"homepage": homepage, "modname": modname})

    if sources is not None and "www.curseforge.com" in sources:
        curseforge_new.append({"sources": sources})
    elif sources is not None and "minecraft.curseforge.com" in sources:
        curseforge_old.append({"sources": sources})
    if sources is not None and "modrinth.com" in sources:
        modrinth.append({"sources": sources, "modname": modname})


def unzip(path, type, modname):
    # 指定要解压的 .jar 文件路径
    jar_file = path

    # 创建 ZipFile 对象
    with zipfile.ZipFile(jar_file, "r") as zip_ref:
        # 解压 .jar 文件中的所有文件
        temp_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_dir)

    if type == 'fabric':
        # 检查临时文件夹中是否存在文件 fabric.mod.json
        fabric_mod_json = os.path.join(temp_dir, "fabric.mod.json")
        if os.path.exists(fabric_mod_json):
            process_fabric_mod_json(fabric_mod_json, modname)

    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)


def upgrade_mods(path, type):
    for dirpath, dirname, filenames in os.walk(path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, "*.jar"):
                modname = filename
                filepath = os.path.join(dirpath, filename)
                unzip(filepath, type, modname)

    # 将分类后的模组信息写入文件
    with open("curseforge_new.json", "w", encoding="utf-8") as f:
        json.dump(curseforge_new, f, ensure_ascii=False, indent=2)

    with open("curseforge_old.json", "w", encoding="utf-8") as f:
        json.dump(curseforge_old, f, ensure_ascii=False, indent=2)

    with open("modrinth.json", "w", encoding="utf-8") as f:
        json.dump(modrinth, f, ensure_ascii=False, indent=2)

    version = input("请输入要升级到的版本号(如:1.19.4):")
    modrinth_spider.run(version, type)
    print('Done!')
