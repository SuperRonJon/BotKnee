import configparser
import os
import ast

from config.botknee_config import BotkneeConfig


class BotConfigParser:

    def __init__(self):
        self.file_path = 'config.ini'
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.file_path):
            print('Found config file')
            self.config.read(self.file_path)
        else:
            print('Could not find config file, creating new one')
            self.create_default_config()
            self.config.read(self.file_path)

    def create_section_map(self, section_title):
        section_map = dict()
        options = self.config.options(section_title)

        for option in options:
            val = self.config.get(section_title, option)

            try:
                section_map[option] = ast.literal_eval(val)
            except ValueError:
                print(f'Could not parse value for {option}, defaulted to None')
                section_map[option] = None

        return section_map

    def get_config(self):
        try:
            botknee_map = self.create_section_map('OPTIONS')
        except Exception:
            print('Error creating config, section not found')
            raise configparser.NoSectionError

        config_map = BotkneeConfig(botknee_map)
        return config_map

    def create_default_config(self):
        config = configparser.ConfigParser()
        config['OPTIONS'] = {"channel": "'sub-games'",
                             "mod_role": "'moderator'",
                             "default_number": "3"}

        with open(self.file_path, 'w') as f:
            config.write(f)
