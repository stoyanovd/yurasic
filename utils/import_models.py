import os

import django


def get_models_from_yurasic_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yurasic.settings")
    django.setup()
    return __import__('songsapp.models').models
