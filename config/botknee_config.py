class BotkneeConfig:

    def __init__(self, botknee_section):
        self.options = DotDict(botknee_section)


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
