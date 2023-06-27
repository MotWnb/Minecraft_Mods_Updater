import os
import json

def get_version_type(version_path):
    with open(version_path, "r", encoding='utf-8') as version_file:
        version_data = json.load(version_file)
        libraries = version_data.get("libraries", [])
        for library in libraries:
            name = library.get("name", "")
            if "fabric" in name.lower() or "sponge" in name.lower():
                return "fabric"
            elif "forge" in name.lower() or "mcp" in name.lower():
                return "forge"
        return ""

def get_versions(folder_path):
    versions_dir = os.path.join(folder_path, "versions")
    versions = []
    for version_dir in os.listdir(versions_dir):
        version_path = os.path.join(versions_dir, version_dir, f"{version_dir}.json")
        if os.path.isfile(version_path):
            versions.append(version_dir)
    return versions
