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

def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


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
    first = await message.reply_text(
        text="`Processing.... Please wait`",
        reply_to_message_id=message.message_id)
    await asyncio.sleep(1)
    fd_msg = await message.forward(
        chat_id=Common().bot_dustbin
    )
    file_name = get_media_file_name(message)
    if message.video is not None:
        file_name_ = message.video.file_name
        file_size = get_size(message.video.file_size)
       # file_size = humanbyte.format_size(message.video.file_size, binary=True)
    elif message.document is not None:
        file_name_ = message.document.file_name
        file_size = get_size(message.document.file_size)
        #file_size = humanbyte.format_size(message.document.file_size, binary=True)

    file_link = f"https://{Common().web_fqdn}/MalluMovies/{fd_msg.message_id}/{file_name}" if Common().on_heroku else \
        f"http://{Common().web_fqdn}:{Common().web_port}/{fd_msg.message_id}"
    await fd_msg.reply_text(
        text=f"**Requested By :** [{message.from_user.first_name}](tg://user?id={message.chat.id})\n**User id :** `{message.from_user.id}`\n**Download Link :** __{file_link}__",
        quote=True,
        disable_web_page_preview=True,
        parse_mode='md'
    )

    await first.edit(
        text=Translation.LINK_TEXT.format(file_name_,file_size,file_link),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"📩 Download Link", url=file_link)],
                [InlineKeyboardButton(text=f"Close 🔐",
                                      callback_data=f"close_btn")]
            ]
        )
    )

@Client.on_callback_query()
async def button(bot, update):
    cb_data = update.data
    if "close_btn" in cb_data:
        await update.message.delete()
    elif "help_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('Home', callback_data='home_btn'),
            InlineKeyboardButton('About', callback_data='about_btn'),
            InlineKeyboardButton('Close', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            parse_mode="html",
            reply_markup=reply_markup,
            disable_web_page_preview=True)
    elif "home_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('Help', callback_data='help_btn'),
            InlineKeyboardButton('About', callback_data='about_btn'),
            InlineKeyboardButton('Close', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.first_name),
            parse_mode="html",
            reply_markup=reply_markup,
            disable_web_page_preview=True)
    elif "about_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('Home', callback_data='home_btn'),
            InlineKeyboardButton('Help', callback_data='help_btn'),
            InlineKeyboardButton('Close', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True)        
        
    
