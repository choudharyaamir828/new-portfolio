from decouple import config

from . import base as base_settings


for setting_name in dir(base_settings):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base_settings, setting_name)


SECRET_KEY = config("SECRET_KEY")
DEBUG = False

# TODO: Configure a production PostgreSQL database before deployment.
