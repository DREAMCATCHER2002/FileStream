import traceback
import asyncio
import humanfriendly as humanbyte
from pyrogram import filters, emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from ...telegram import Common
from translation import Translation
from ..utils import filters
from mega.database.database import is_user_exist, add_user, ban_user, remove_ban, get_all_banned_users


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

@Client.on_message(filters.private & filters.command(["ban"]))
async def ban(c, m):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\nUsage:\n\n`/ban user_id ban_duration ban_reason`\n\nEg: `/ban 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
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
                f"**#Banned**\n\n**Duration: `{ban_duration} day(s)`\n**Reason :** `{ban_reason}`"
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

@Client.on_message(filters.private & filters.command(["unban"]))
async def unban(c, m):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\nUsage:\n\n`/unban user_id`\n\nEg: `/unban 1234567`\n This will unban user with id `1234567`.",
            quote=True
        )
        return
    
    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        
        try:
            await c.send_message(
                user_id,
                f"**#Unbanned**\n\n__**You Unbanned enjoy**__"
            )
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

@Client.on_message(filters.private & filters.command(["banned_users"]))
async def _banned_usrs(c, m):
    all_banned_users = await get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"° **user_id**: `{user_id}`\n**Ban Duration**: `{ban_duration}`\n**Banned on**: `{banned_on}`\n**Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)

#@Client.on_message(group=-1)
#async def stop_user_from_doing_anything(_, message: Message):
#    allowed_users = Common().allowed_users
#    if allowed_users and message.from_user.id not in allowed_users:
#        message.stop_propagation()
#    else:
#        message.continue_propagation()
