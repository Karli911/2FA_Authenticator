import json
import os

class LanguageManager:
    def __init__(self, language_dir='languages', default_language='en'):
        self.language_dir = language_dir
        self.current_language = default_language
        self.translations = self.load_language(default_language)

    def load_language(self, language_code):
        language_file = os.path.join(self.language_dir, f'{language_code}.json')
        if os.path.exists(language_file):
            with open(language_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"Language file {language_file} not found.")

    def set_language(self, language_code):
        self.translations = self.load_language(language_code)
        self.current_language = language_code

    def get_translation(self, key):
        keys = key.split('.')
        value = self.translations
        for k in keys:
            value = value.get(k, {})
        return value if value else key