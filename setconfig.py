import json

# 读取配置文件
def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，则返回空字典
        return {}

# 写入配置文件
def write_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)

# 获取配置值
def get_config(key):
    config = read_config()
    return config.get(key)

# 设置配置值
def set_config(key, value):
    config = read_config()
    config[key] = value
    write_config(config)
    if key == "isolation_enabled":
        print("版本隔离已开启" if value else "版本隔离未开启")
