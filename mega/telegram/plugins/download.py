import time
import urllib.parse
from mega.common import Common
from pyrogram import Client, enums, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from translation import Translation
from mega.database.database import get_ban_status

GAP = {}

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

async def check_time_gap(user_id: int):
    """A Function for checking user time gap!
    :parameter user_id Telegram User ID"""

    if str(user_id) in GAP:
        current_time = time.time()
        previous_time = GAP[str(user_id)]
        if round(current_time - previous_time) < Common().time_gap:
            return True, round(previous_time - current_time + Common().time_gap)
        elif round(current_time - previous_time) >= Common().time_gap:
            del GAP[str(user_id)]
            return False, None
    elif str(user_id) not in GAP:
        GAP[str(user_id)] = time.time()
        return False, None


@Client.on_message(filters.private & filters.document | filters.video)
async def download_user(bot: Client, message: Message):
    first = await message.reply_text(
        text="`Generating Download Link....`",
        reply_to_message_id=message.id)
    ban_status = await get_ban_status(message.chat.id)
    if ban_status['is_banned']:
        await first.edit_text(
            f"**Sorry Dear 😞, You are Banned to Use Me.\n\n🤦 Ban Reason : {ban_status['ban_reason']}**"
        )
        return
    f_channel = await bot.get_chat(Common().force_sub)
    if f_channel.username is None:
        update_channel = Common().force_sub
        jn_link = await bot.export_chat_invite_link(update_channel)
        try:
            chat = await bot.get_chat_member(update_channel, message.chat.id)
            if chat.status=='kicked':
                return
        except UserNotParticipant:
            await first.delete()
            btn = [[
                InlineKeyboardButton('📢 Join Project Channel 📢', url=jn_link)
            ]]
            reply = InlineKeyboardMarkup(btn)
            await message.reply_photo(
                photo="https://te.legra.ph/file/f838b9c4154a9f539958a.jpg",
                caption=Translation.JOIN.format(message.from_user.mention),
                reply_markup=reply)
            return
    else:
        try:
            chat = await bot.get_chat_member(f_channel.username, message.chat.id)
            if chat.status=='kicked':
                return False
        except UserNotParticipant:
            await first.delete()
            btn = [[
                InlineKeyboardButton('📢 Join Project Channel 📢', url=f"https://t.me/{f_channel.username}")
            ]]
            reply = InlineKeyboardMarkup(btn)
            await message.reply_photo(
                photo="https://te.legra.ph/file/f838b9c4154a9f539958a.jpg",
                caption=Translation.JOIN.format(message.from_user.mention),
                reply_markup=reply)
            return
    is_in_gap, sleep_time = await check_time_gap(message.from_user.id)
    if is_in_gap:
        await first.edit_text("<b>Sorry Sir 😍</b>\n\n"
                           "<b>No Flooding Allowed! 🤒</b>\n\n"
                           f"<b>Please Wait  ⏰  `{str(sleep_time)}second`  ⏰  For Send New File !! 🤸</b>")
        return
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

    file_link = f"https://{Common().web_fqdn}/WhitE_DeviL09/{fd_msg.id}/{file_name}" if Common().on_heroku else \
        f"http://{Common().web_fqdn}:{Common().web_port}/{fd_msg.id}"
    await fd_msg.reply_text(
        text=f"**Requested By :** [{message.from_user.first_name}](tg://user?id={message.chat.id})\n**User id :** `{message.from_user.id}`\n**Download Link :** __{file_link}__",
        quote=True,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

    await first.edit(
        text=Translation.LINK_TEXT.format(file_name_,file_size,file_link),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"📤 Download Link 📤", url=file_link)],
                [InlineKeyboardButton(text=f"🔐 Close This Link 🔐",
                                          callback_data=f"close_btn")]
            ]
        )
    )

@Client.on_callback_query()
async def button(bot, update: CallbackQuery):
    cb_data = update.data
    if "close_btn" in cb_data:
        await update.message.delete()
    elif "help_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('🏘️ Home', callback_data='home_btn'),
            InlineKeyboardButton('⚙️ About', callback_data='about_btn'),
            InlineKeyboardButton('Close 🔐', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True)
    elif "home_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('⚒️ Help', callback_data='help_btn'),
            InlineKeyboardButton('⚙️ About', callback_data='about_btn'),
            InlineKeyboardButton('Close 🔐', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.first_name),
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True)
    elif "about_btn" in cb_data:
        btn = [[
            InlineKeyboardButton('🏘️ Home', callback_data='home_btn'),
            InlineKeyboardButton('⚒️ Help', callback_data='help_btn'),
            InlineKeyboardButton('Close 🔐', callback_data='close_btn')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True)        
        
    
