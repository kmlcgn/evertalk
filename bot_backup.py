from pyrogram import Client, filters, idle
from pyrogram.types import Message # To make easier to code.
from random import choice as randomchoice
from pyrogram.enums import ChatType
from uuid import uuid4
from io import BytesIO
import openai
from utils.config import *
from utils.mongo import add_msg, add_filter, get_filters, del_filter, del_all_filters


# Two clients for listening and responding.
bot = Client("ListenerBot", API_ID,API_HASH, bot_token=BOT_TOKEN)


if OPENAI_KEY : openai.api_key = OPENAI_KEY
else : print("You haven't added an openAI API key")

SUDO = [int(x) for x in (SUDO_ID).split()] # SUDO Users. (Users who can add auto replys.) Don't edit this part.

@bot.on_message(filters.command(["start","help"]))
async def startmsg(_, message:Message):
    if message.from_user :
        if message.from_user.id in SUDO : 
            await message.reply_text("""Hello I am auto responder bot.

Sudo only commands :            
 • /start or /help - This menu
 • /filter `keyword or sentence` - To add fiters.
 • /filters - To get current filters and filter ids.
 • /delfilter `filter id` - To delete a filter.
 • /clearfilters - To dellet all filters.

Note : This bot will auto generate a respond using ChatGPT for added filters and user account will send the reply.
            """)
            return
    await message.reply_text("You can do nothing by sending that command.")

@bot.on_message(filters.command("filter"))
async def add_filter_msg(_, message:Message):
    if not message.from_user : return
    if not message.from_user.id in SUDO : return
    if len(message.command) < 2:
        await message.reply_text("Give something for filter.", quote=True)
        return
    msg_text_split = message.text.split()
    keyword = ' '.join(msg_text_split[1:])
    keyword.lower()
    filter_id = str(uuid4())[:8]
    add_filter(keyword, filter_id)
    await message.reply_text(f"`{keyword}` added as a filter.")    

@bot.on_message(filters.command("filters"))
async def get_filters_msg(_, message:Message):
    if not message.from_user : return
    if not message.from_user.id in SUDO : return
    sendmsg = await message.reply_text("Processing 🔄")
    filter_string = ""
    get_filters_in_db = get_filters()
    for filterr in get_filters_in_db :
        filter_id = filterr["filter_id"]
        filter_keys = filterr["keyword"]
        filter_string += f"• `{filter_id}` : {filter_keys}\n"
    if filter_string == "" : filter_string = "No filters were added."
    else : filter_string += "Use `/delfilter filterid` to delete a filter."    
    if len(filter_string) > 4096 :
        await sendmsg.delete()
        with BytesIO(str.encode(filter_string.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True)
        return
    await sendmsg.edit(filter_string)

@bot.on_message(filters.command("delfilter"))
async def delete_afilter(_, message:Message):
    if not message.from_user : return
    if not message.from_user.id in SUDO : return    
    text_split = message.text.split()
    if len(text_split) < 2 : return await message.reply_text("Give a filter id to delete a filter")
    filter_id = text_split[1]
    del_filter(filter_id)
    await message.reply_text("Deleted filter.")

@bot.on_message(filters.command("clearfilters"))
async def clear_allfilters(_, message:Message):
    if not message.from_user : return
    if not message.from_user.id in SUDO : return    
    sendmsg = await message.reply_text("Processing 🔄")
    del_all_filters()
    await sendmsg.edit("All filters removed.")

@bot.on_message(group=1) #
async def listenmessages(_, message:Message):  
    if message.chat.type != ChatType.PRIVATE :
        msg_text = None
        photo_id = None
        video_id = None
        document_id = None
        sticker_id = None
        if message.text : msg_text = message.text
        if message.caption : msg_text = message.caption
        if message.photo : photo_id = message.photo.file_id
        if message.video : video_id = message.video.file_id
        if message.document : document_id = message.document.file_id
        if message.sticker : sticker_id = message.sticker.file_unique_id
        add_msg(message.chat.id, message.id,msg_text,photo_id,video_id,document_id,sticker_id)
    if not message.text : return
    if message.from_user :
        if message.from_user.id == SESSION_USER_ID : return
    if message.text.startswith("/") : return
    message.text.lower()
    textinmsg = message.text
    is_matching = False
    query_as_list = get_filters()
    try : 
        for file in query_as_list : 
            keyword_list = (file['keyword']).split()
            for keyy in keyword_list: 
                if keyy not in textinmsg: 
                    is_matching = False
                    break
                is_matching = True
            if is_matching : break    
    except : pass
    if is_matching :
        if not OPENAI_KEY : return print("You haven't added an openAI API key")
        prompt = message.text
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5)
        response = completion.choices[0].text
        random_session = randomchoice(STRING_SESSION)
        userbot = Client(random_session[0], API_ID,API_HASH, session_string=random_session[1] ,in_memory=True)
        async with userbot : await userbot.send_message(message.chat.id, response, reply_to_message_id=message.id)


# User friendly start and stop
bot.start() ; print("Listener Bot Started.")
idle() ; bot.stop ; print("Listener Bot Stoppped.")