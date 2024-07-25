import json

def load_settings(settings_file):
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
    else:
        settings = {}
    return settings

def save_settings(settings, settings_file):
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)