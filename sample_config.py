import os

class Config(object):
    # add config vars for database
    DB_URI = os.environ.get("DATABASE_URL", "")
    OWNER = [int(i) for i in os.environ.get("OWNER", "809546777").split(" ")]  

