import traceback
import asyncio
import humanfriendly as humanbyte
from pyrogram import filters, emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from ...telegram import Common
from translation import Translation
from ..utils import filters


@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text="Hai im file to link bot")

@Client.on_message(filters.command(["help"]))
async def help_user(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT.format(
                update.from_user.first_name),
        parse_mode="html")

@Client.on_callback_query(filters.regex(r'^help_btn$'))
async def help_button(bot, update):
    await update.answer()
    buttons = [[
        InlineKeyboardButton('📌 Support Group', url='https://t.me/Dx_Support'),
        InlineKeyboardButton('Update Channel 📜', url='https://t.me/DX_Botz')
        ],[
        InlineKeyboardButton('♻️Share', url='tg://msg?text=**Hey%20Broh**%F0%9F%A5%B0%2C%0A__This%20Bot%20Generate%20Instant%20File%20Direct%20Download%20Link__%F0%9F%94%A5%0A%0A**Bot%20Link**%20%3A-%20%40FileToLinkDXBot'),
        InlineKeyboardButton('Close 🔐', callback_data='cancel_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.edit_message_text(
        text=Translation.HELP_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode="html")

@Client.on_callback_query(filters.regex(r'^cancel_btn$'))
async def cancel(bot, update):
    """Cancel and delete message"""
    await update.answer()
    #await message.delete()
    await update.message.delete()

@Client.on_message(group=-1)
async def stop_user_from_doing_anything(_, message: Message):
    allowed_users = Common().allowed_users
    if allowed_users and message.from_user.id not in allowed_users:
        message.stop_propagation()
    else:
        message.continue_propagation()
