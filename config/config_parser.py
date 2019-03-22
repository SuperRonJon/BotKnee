import configparser
import os
import ast

from config.botknee_config import BotkneeConfig


class BotConfigParser:

    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        if os.path.isfile(file_path):
            self.config.read(file_path)
        else:
            print('Could not find config file...')
            assert os.path.exists(file_path), 'Cannot resolve config path'

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
