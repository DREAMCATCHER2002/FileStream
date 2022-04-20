import os
import re
import time
import secrets
import asyncio
import logging
import humanfriendly as size
import humanfriendly as humanbyte
import urllib.parse
from sample_config import Config
from mega.common import Common
from pyrogram import emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from mega.telegram.utils.custom_download import TGCustomYield
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from translation import Translation

from ..utils import filters

def get_media_file_name(message):
    media = message.video or message.document
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@Client.on_message(filters.document | filters.video)
async def download_user(bot, message):

    try:
        chat = await bot.get_chat_member("Dx_Botz", message.chat.id)
        if chat.status=='kicked':
         #   if bot.sent_message:
                #await reply('You are banned!')
            await bot.send_message(
                chat_id=message.chat.id,
                text=Translation.KICK,
                reply_to_message_id=message.message_id
         )
            return false
    except UserNotParticipant:
    #    if bot.sent_message:
         await bot.send_message(
            chat_id=message.chat.id,
            text=Translation.JOIN,
            reply_to_message_id=message.message_id,
            reply_markup=InlineKeyboardMarkup(
             [
                [
                    InlineKeyboardButton('😎 Join Channel 😎', url='https://t.me/Dx_BotZ'),
                ]
             ]
            )
         )
         return
    first = await message.reply_text("`Processing.... Please wait`")
    await asyncio.sleep(1)
    fd_msg = await message.forward(
        chat_id=Common().bot_dustbin
    )
    await bot.send_message(
        Config.CHANNEL_ID,
        f"**This File☝️ Sender Name :-** [{message.from_user.first_name}](tg://user?id={message.chat.id})"
    )
    file_name = get_media_file_name(message)
    if message.video is not None:
        file_name_ = message.video.file_name
        file_size = message.video.file_size
        file_size = humanbyte.format_size(message.video.file_size, binary=True)
    elif message.document is not None:
        file_name_ = message.document.file_name
        file_size = message.document.file_size
        file_size = humanbyte.format_size(message.document.file_size, binary=True)

    file_link = f"https://{Common().web_fqdn}/MalluMovies/{fd_msg.message_id}/{file_name}" if Common().on_heroku else \
        f"http://{Common().web_fqdn}:{Common().web_port}/{fd_msg.message_id}"

    await first.edit(
        text=Translation.LINK_TEXT + Translation.FILE_NAME.format(file_name_) + Translation.FILE_SIZE.format(file_size) + Translation.FILE_LINK.format(file_link),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"📩 Download Link", url=file_link)],
                [InlineKeyboardButton(text=f"Close 🔐",
                                      callback_data=f"cancel_btn")]
            ]
        )
    )

@Client.on_callback_query()
async def button(bot, update):
    cb_data = update.data
    if "cancel_btn" in cb_data:
        await update.message.delete()
    
