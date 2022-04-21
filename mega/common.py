import ast
import configparser
import os


class Common:
    def __init__(self):
        """Common: are commonly shared variables across the application that is loaded from the config file or env."""
        self.working_dir = "mega/working_dir"
        self.on_heroku = False

        self.is_env = bool(os.environ.get("ENV", None))
        if self.is_env:
            self.tg_app_id = int(os.environ.get("TG_APP_ID"))
            self.tg_api_key = os.environ.get("TG_API_HASH")

            self.bot_session = ":memory:"
            self.bot_api_key = os.environ.get("TG_BOT_TOKEN")
            self.bot_dustbin = int(os.environ.get("TG_DUSTBIN_CHAT", "-100"))
            self.allowed_users = ast.literal_eval(
                os.environ.get("ALLOWED_USERS", '[]')
            )
            self.owner = [int(i) for i in os.environ.get("OWNER", "809546777").split(" ")]
            self.database_url = os.environ.get("DATABASE_URL")
            self.force_sub = int(os.environ.get("FORCE_SUB_CHANNEL", "-100"))
            self.is_atlas = os.environ.get('IS_ATLAS', None)

            self.web_port = os.environ.get("WEB_SERVER_PORT", 8080)
            if 'DYNO' in os.environ:
                self.on_heroku = True
                self.web_port = os.getenv("PORT", 8080)
            self.web_bind_address = os.environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0")
            self.web_fqdn = os.environ.get("WEB_SERVER_FQDN", self.web_bind_address)
        else:
            self.app_config = configparser.ConfigParser()

            self.app_config_file = "mega/working_dir/config.ini"
            self.app_config.read(self.app_config_file)

            self.tg_app_id = int(self.app_config.get("pyrogram", "api_id"))
            self.tg_api_key = self.app_config.get("pyrogram", "api_hash")

            self.bot_session = self.app_config.get("bot-configuration", "session")
            self.bot_api_key = self.app_config.get("bot-configuration", "api_key")
            self.bot_dustbin = int(self.app_config.get("bot-configuration", "dustbin"))
            self.allowed_users = ast.literal_eval(
                self.app_config.get("bot-configuration", "allowed_users", fallback='[]')
            )

            self.is_atlas = self.app_config.getboolean('database', 'is_atlas', fallback=False)

            self.web_bind_address = self.app_config.get("web_server", "bind_address", fallback="0.0.0.0")
            self.web_port = int(self.app_config.get("web_server", "port", fallback=8080))
            self.web_fqdn = self.app_config.get("web_server", "fqdn", fallback=self.web_bind_address)
