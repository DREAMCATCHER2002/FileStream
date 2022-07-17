import ast
import configparser
import os


class Common:
    def __init__(self):
        """Common: are commonly shared variables across the application that is loaded from the config file or env."""
        self.working_dir = "mega/working_dir"
        self.on_heroku = False

        self.is_env = bool(os.environ.get("ENV", None))
        if not self.is_env:
            self.app_config_file = "mega/working_dir/config.env"
            from dotenv import load_dotenv
            load_dotenv(self.app_config_file)

        self.tg_app_id = int(os.environ.get("TG_APP_ID"))
        self.tg_api_key = os.environ.get("TG_API_HASH")

        self.bot_session = os.environ.get("SESSION", ":memory:")
        self.in_memory = self.bot_session == ":memory:"
        self.bot_session = self.bot_session if not self.in_memory else "my_session"

        self.bot_api_key = os.environ.get("TG_BOT_TOKEN")
        self.bot_dustbin = int(os.environ.get("TG_DUSTBIN_CHAT", "-100"))
        self.allowed_users = ast.literal_eval(
            os.environ.get("ALLOWED_USERS", '[]')
        )
        self.owner = [int(i) for i in os.environ.get("OWNER", "809546777").split(" ")]
        self.database_url = os.environ.get("DATABASE_URL")
        self.force_sub = int(os.environ.get("FORCE_SUB_CHANNEL", "-100"))
        self.time_gap = int(os.environ.get("TIME_GAP"))
        self.is_atlas = os.environ.get('IS_ATLAS', None)

        self.web_port = os.environ.get("WEB_SERVER_PORT", 8080)
        if 'DYNO' in os.environ:
            self.on_heroku = True
            self.web_port = os.getenv("PORT", 8080)
        self.web_bind_address = os.environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0")
        self.web_fqdn = os.environ.get("WEB_SERVER_FQDN", self.web_bind_address)

