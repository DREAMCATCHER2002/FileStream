import traceback
import asyncio
import humanfriendly as humanbyte
from pyrogram import filters, emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from ...telegram import Common
from translation import Translation
from ..utils import filters
from mega.database.database import is_user_exist, add_user


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await is_user_exist(update.chat.id):
        await add_user(update.chat.id)
        await bot.send_message(
            chat_id=Common().bot_dustbin,
            text=f"**#NEWUSER**\n**{update.from_user.mention}",
            parse_mode='md')        
    btn = [[
        InlineKeyboardButton('Help', callback_data='help_btn'),
        InlineKeyboardButton('About', callback_data='about_btn'),
        InlineKeyboardButton('Close', callback_data='close_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await update.reply_photo(
        photo='https://te.legra.ph/file/e5830830ab2f987e694c0.jpg',
        caption=Translation.START_TEXT.format(update.from_user.first_name),
        parse_mode="html",
        reply_markup=reply_markup)

@Client.on_message(filters.private & filters.command(["help"]))
async def help_user(bot, update):
    btn = [[
        InlineKeyboardButton('Home', callback_data='home_btn'),
        InlineKeyboardButton('About', callback_data='about_btn'),
        InlineKeyboardButton('Close', callback_data='close_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT.format(
                update.from_user.first_name),
        parse_mode="html",
        reply_markup=reply_markup,
        disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command(["about"]))
async def about_user(bot, update):
    btn = [[
        InlineKeyboardButton('Home', callback_data='home_btn'),
        InlineKeyboardButton('Help', callback_data='help_btn'),
        InlineKeyboardButton('Close', callback_data='close_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await update.reply_text(
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        disable_web_page_preview=True)

#@Client.on_message(group=-1)
#async def stop_user_from_doing_anything(_, message: Message):
#    allowed_users = Common().allowed_users
#    if allowed_users and message.from_user.id not in allowed_users:
#        message.stop_propagation()
#    else:
#        message.continue_propagation()
