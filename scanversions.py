import os
import json

def get_version_type(version_path):
    with open(version_path, "r") as version_file:
        version_data = json.load(version_file)
        libraries = version_data.get("libraries", [])
        for library in libraries:
            name = library.get("name", "")
            if "fabric" in name.lower() or "sponge" in name.lower():
                return "Fabric"
            elif "forge" in name.lower() or "mcp" in name.lower():
                return "Forge"
        return ""

def get_versions(folder_path):
    versions_dir = os.path.join(folder_path, "versions")
    versions = []
    for version_dir in os.listdir(versions_dir):
        version_path = os.path.join(versions_dir, version_dir, f"{version_dir}.json")
        if os.path.isfile(version_path):
            version_type = get_version_type(version_path)
            version_name = version_dir
            if version_type != "":
                version_name += f" ({version_type})"
            versions.append(version_name)
    return versions
