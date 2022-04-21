import traceback
import asyncio
import time
import humanfriendly as humanbyte
from pyrogram import filters, emoji, Client
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ...telegram import Common
from translation import Translation
from ..utils import filters
from mega.database.database import is_user_exist, add_user, ban_user, remove_ban, get_all_banned_users, get_ban_status, total_users_count

BOT_START_TIME = time.time()


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await is_user_exist(update.chat.id):
        await add_user(update.chat.id)
        await bot.send_message(
            chat_id=Common().bot_dustbin,
            text=f"<b>#NEWUSER</b>\n<b>Name : {update.from_user.mention}</b>\n<b>User id :</b> <code>{update.from_user.id}</code>",
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

@Client.on_message(filters.private & filters.command('ban'))
async def banuser(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a user id</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "<b>No reason Provided 🤔</b>"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an invalid user, make sure ia have met him before.</b>")
    except IndexError:
        return await message.reply("<b>This might be a channel, make sure its a user.</b>")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is already banned\n\nReason : {jar['ban_reason']}</b>")
        await ban_user(k.id, reason)
        await message.reply(f"<b>Successfully Banned : {k.mention} ✔️</b>")
        await bot.send_message(
            Common().bot_dustbin,
            f"<b>Uꜱᴇʀ Nᴀᴍᴇ : [{k.mention}](tg://user?id={k.id})\nUꜱᴇʀ ɪᴅ : {k.id}\nSᴛᴀᴛᴜꜱ : #Banned ✔️\nBᴀɴ Rᴇᴀꜱᴏɴ : {reason}\nTɪᴍᴇ Lɪᴍɪᴛ : Permanent</b>"
        )
  
@Client.on_message(filters.private & filters.command('unban'))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a user id</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "<b>No Reason Provided</b> 🤔"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an invalid user, make sure ia have met him before.</b>")
    except IndexError:
        return await message.reply("<b>Thismight be a channel, make sure its a user.</b>")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is not yet banned.</b>")
        await remove_ban(k.id)
        await message.reply(f"<b>Successfully Unbanned : {k.mention} 🤝</b>")

@Client.on_message(filters.private & filters.command(["banlist"]))
async def _banned_usrs(c, m):
    all_banned_users = await get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"° **user_id**: `{user_id}`\n**Reason**: `{ban_reason}`\n\n"
    reply_text = f"**Total banned user(s):** `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)

@Client.on_message(filters.private & filters.command(["status"]))
async def stats(bot, update):
    total_users = await total_users_count()
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    all_banned_users = await get_all_banned_users()
    banned_usr_count = 0
    async for banned_user in all_banned_users:
        banned_usr_count += 1
    text = f"""`Uptime : {currentTime}
Disk space : {total}
Used : {used}
Free : {free}

Total Users : {total_users}
Banned Users : {banned_usr_count}`"""
    await update.reply_text(text)

#@Client.on_message(group=-1)
#async def stop_user_from_doing_anything(_, message: Message):
#    allowed_users = Common().allowed_users
#    if allowed_users and message.from_user.id not in allowed_users:
#        message.stop_propagation()
#    else:
#        message.continue_propagation()
