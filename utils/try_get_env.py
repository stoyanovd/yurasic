import os

import configparser


# https://docs.python.org/3/library/configparser.html

def try_get_env(env_file):
    if not os.path.exists(env_file):
        return
    config = configparser.ConfigParser()
    config.read(env_file)

    print('Parse env file: "', env_file, '"')

    default_keyword = 'DEFAULT'
    print('Currently only its ', default_keyword, ' section')

    for k, v in config[default_keyword].items():
        k = k.upper()

        # TODO not beautiful hack
        v = v.strip('"')
        v = v.strip("'")

        os.environ[k] = v

        print('SET ', k, ' as ', v)
