import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = True
    TESTING = False
    PERMANENT_SESSION_LIFETIME = 600
    # PATH_TO_EQUIPMENT = os.path.join(os.path.dirname(BASEDIR), "coursework_5/data/equipment.json")
    PATH_TO_EQUIPMENT = os.path.join(os.path.dirname(BASEDIR), "code/data/equipment.json")
