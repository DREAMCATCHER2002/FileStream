import os

class Config(object):
    # add config vars for the log channel
    CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 12345))
    DUSTBIN_ID = int(os.environ.get("DUSTBIN_ID", 12345))
    UTUBE_BOT_USERS = ["1155642873"]
    # dict to hold the ReQuest queue
    ADL_BOT_RQ = {}
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 60
