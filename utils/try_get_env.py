import os

import configparser


def try_get_env(env_file):
    if not os.path.exists(env_file):
        return
    config = configparser.ConfigParser()
    config.read(env_file)
    default_keyword = 'DEFAULT'
    for k, v in config[default_keyword].items():
        k = k.upper()
        os.environ[k] = v
