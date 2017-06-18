import os

# import configparser

import yaml


# https://docs.python.org/3/library/configparser.html

def try_get_env(env_file):
    if not os.path.exists(env_file):
        return
    # config = configparser.ConfigParser()
    # config.read(env_file)

    with open(env_file) as f:
        d = yaml.load(f.read())

    print('Parse env file: "', env_file, '"')

    # default_keyword = 'DEFAULT'
    # print('Currently only its ', default_keyword, ' section')

    print(d)

    for k, v in d.items():
        k = k.upper()

        # TODO not beautiful hack
        # v = v.strip('"')
        # v = v.strip("'")

        os.environ[k] = v

        print('SET ', k, ' as ', v)
