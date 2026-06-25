import yaml
import os
from filelock import FileLock

PC_DEBUG = True

# if PC_DEBUG:
#     # home_dir = os.path.expanduser("~")
#     current_file_path = os.path.abspath(__file__)
#     current_dir = os.path.dirname(current_file_path)
#     parent_path = os.path.dirname(current_dir)
#     CONFIG_PATH = parent_path + "/config.yaml"
#     LOCK_PATH = CONFIG_PATH + ".lock"
# else:
#     CONFIG_PATH = "config.yaml"
#     CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml")
#     LOCK_PATH = CONFIG_PATH + ".lock"


CONFIG_PATH = "config.yaml"
# LOCK_PATH = CONFIG_PATH + ".lock"

def retrieve_yaml_file():
    config = {}
    # print(LOCK_PATH)
    # print(CONFIG_PATH)
    try:
        # with FileLock(LOCK_PATH):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                config = yaml.safe_load(file) or {}
    except Exception as e:
        print(f"⚠️ Error reading YAML file: {e}")

    return config

# #   YAML functions
# def update_yaml_flag(TAGlvl1, TAGlvl2, value):
#     try:
#         with FileLock(LOCK_PATH):
#             with open(CONFIG_PATH, 'r') as f:
#                 config = yaml.safe_load(f) or {}

#             # Check of de eerste en tweede tag bestaan
#             if TAGlvl1 not in config or TAGlvl2 not in config[TAGlvl1]:
#                 raise KeyError(f"'{TAGlvl1}' or '{TAGlvl2}' not found in config")

#             # Pas de waarde aan
#             config[TAGlvl1][TAGlvl2] = value

#             # Schrijf het bestand terug
#             with open(CONFIG_PATH, 'w') as f:
#                 yaml.safe_dump(config, f, default_flow_style=False)
#                 # print(f"✓ Updated {TAGlvl1} -> {TAGlvl2} to {value} in config.yaml")

#     except Exception as e:
#         print(f"⚠️ Failed to update config: {e}")