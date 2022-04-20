from . database import Db
from sample_config import Config

Db.dburl = Config.DB_URI
db = Db()
