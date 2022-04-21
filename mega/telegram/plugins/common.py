import traceback
import asyncio
import humanfriendly as humanbyte
from pyrogram import filters, emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from ...telegram import Common
from translation import Translation
from ..utils import filters
from mega.database.database import is_user_exist, add_user, ban_user


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await is_user_exist(update.chat.id):
        await add_user(update.chat.id)
        await bot.send_message(
            chat_id=Common().bot_dustbin,
            text=f"<b>#NEWUSER</b>\n<b>{update.from_user.mention}</b>",
            parse_mode='html')        
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

@Client.on_message(filters.private & filters.command(["ban_user"]))
async def ban(c, m):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return
    
    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        
        try:
            await c.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

#@Client.on_message(group=-1)
#async def stop_user_from_doing_anything(_, message: Message):
#    allowed_users = Common().allowed_users
#    if allowed_users and message.from_user.id not in allowed_users:
#        message.stop_propagation()
#    else:
#        message.continue_propagation()
