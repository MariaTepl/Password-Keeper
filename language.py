import json


class LanguageManager:
    def __init__(self):
        self.current_lang = 'ru'
        self.translations = {}
        self.load_language('ru')

    def load_language(self, lang_code):
        try:
            with open(f'data/translations/{lang_code}.json', 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
                self.current_lang = lang_code
        except Exception as e:
            print(f"Error loading language: {e}")

