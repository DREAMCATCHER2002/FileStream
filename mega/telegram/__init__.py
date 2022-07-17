"""MegaDLBot Pyrogram Client."""
from pyrogram import Client
from mega.common import Common


MegaDLBot = Client(
    name=Common().bot_session,
    in_memory=Common().in_memory,
    api_id=Common().tg_app_id,
    api_hash=Common().tg_api_key,
    bot_token=Common().bot_api_key,
    workers=200,
    workdir=Common().working_dir,
    plugins=dict(root="mega/telegram/plugins")
)
