from importlib import import_module


class Settings(object):
    def __init__(self):
        setting_module = import_module("core.settings")
        for setting in dir(setting_module):
            if setting.isupper():
                settingValue = getattr(setting_module, setting)
                setattr(self, setting, settingValue)


settings = Settings()