#!/usr/bin/env python3
import os
import sys

from utils.try_get_env import try_get_env

if __name__ == "__main__":
    try_get_env('.env')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yurasic.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
