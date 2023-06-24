import os
import json
import fnmatch
import zipfile
import tempfile
import simplejson as json

def unzip(path, type):
    # 指定要解压的 .jar 文件路径
    jar_file = path

    # 创建 ZipFile 对象
    with zipfile.ZipFile(jar_file, "r") as zip_ref:
        # 解压 .jar 文件中的所有文件
        temp_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_dir)
    
    if type == 'Fabric':
    # 检查临时文件夹中是否存在文件 fabric.mod.json
        fabric_mod_json = os.path.join(temp_dir, "fabric.mod.json")
        if os.path.exists(fabric_mod_json):
            print("找到fabric.mod.json")
            with open(fabric_mod_json, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误：{e}")
                    return

            homepage = data.get("contact", {}).get("homepage")
            sources = data.get("contact", {}).get("sources")

            # 输出结果
            if homepage:
                print("homepage:", homepage)
            if sources:
                print("sources:", sources)
                

        else:
            print("未找到fabric.mod.json")


    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)



def upgrade_mods(path, type):
    # 在这里添加您更新 Minecraft 模组的代码
    # print(f"正在更新版本为 '{path}' 的 Minecraft 模组...")
    for dirpath, dirname, filenames in os.walk(path):
        # 遍历当前目录下的所有文件
        for filename in filenames:
            # 判断文件名是否以 .jar 结尾
            if fnmatch.fnmatch(filename, "*.jar"):
                # 如果是 .jar 文件，则输出文件路径
                print('发现一个mod:', filename)
                filepath = os.path.join(dirpath, filename)
                unzip(filepath, type)
