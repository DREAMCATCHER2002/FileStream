import os

class Config(object):
    # add config vars for database
    DB_URI = os.environ.get("DATABASE_URL", "")
