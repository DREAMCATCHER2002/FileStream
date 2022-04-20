from .. database import Db
from bot.config import Config

Db.dburl = Config.DB_URI
db = Db()
