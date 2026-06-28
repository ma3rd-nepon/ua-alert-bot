from pyrogram import *
from pyrogram.errors import MessageTooLong
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from src.utils.utils import *
from io import BytesIO

import requests
import json

client = Client(name=gfc("name"),
                api_id=gfc("api_id"),
                api_hash=gfc("api_hash"),
                bot_token=gfc("bot_token")
        )

prefix = "/"
comm_pref = gfc("prefix")
interval = 43200
schedule_text = "/grow"
image = "assets/map.png"
ADM_LIST = [] # Your User IDs admins
main_chat = gfc("main_chat")
alert = False
maps_site = "https://alerts.com.ua/map.png" # UNAVAIABLE SITE 
file_id_idk = "CAACAgIAAxkBAAMPZmWivOBjcNMsqZQ_gBH1j3eMYvEAAkciAALYQahKjCShe_CVt-seBA"

with open("src/utils/ukraine_language.json", "r", encoding="utf-8") as f:
    lang = json.load(f)


def filter_startwith(query):
    """Filter for check that message starts with word (or list words)"""
    async def filtor(self, client, message):
        if message.text:
            target = (message.text.split(" ", maxsplit=1)[0]).lower()
            return target == self.query if type(self.query) == str else target in self.query
        return False

    return filters.create(filtor, query=query)


async def grow():
    await client.send_message(chat_id=main_chat,
                              text=schedule_text)


def download_map():
    img = requests.get(maps_site).content
    with open("assets/map.png", "wb+") as file:
        file.write(img)
    # logging.debug("New map downloaded")


async def check_alerts():
    if check_regions() and not alert:
        file_id = file_id_idk
        alert = True

        await client.send_sticker(chat_id=main_chat, sticker=file_id)

    elif alert and not check_regions():
        file_id = file_id_idk

        alert = False

        await client.send_sticker(chat_id=main_chat, sticker=file_id)


@client.on_message(filters.command("start", prefix))
async def greetings(_, message):
    return await message.reply(lang["greeting"])


@client.on_message(filters.command("map", prefix))
async def send_map_alerts(_, message):
    """Reply a alert map"""
    return await client.send_photo(chat_id=message.chat.id, photo=image)


@client.on_message(filters.command("sticker", prefix))
async def send_sticker_by_file_id(_, message):
    """Send sticker through File ID"""
    try:
        file_id = message.text.split(" ", maxsplit=1)[1]
    except:
        file_id = file_id_idk
    return await client.send_sticker(chat_id=message.chat.id, sticker=file_id)


@client.on_message(filters.command("message", comm_pref))
async def send_msg_json(_, message):
    """Reply a message.json"""
    try:
        text = "```json" + str(message) + "```"
        return await message.reply(text)
    except MessageTooLong:
        filename = hash_name(message)
        with open(f"messages/{filename}.txt", "w+") as file:
            file.write(str(message))
        return await client.send_document(chat_id=message.chat.id, document=f"messages/{filename}.txt")


@client.on_message(filters.command("file_id", prefix))
async def get_file_id(_, message):
    """Send File ID"""
    m = message.reply_to_message
    typ = message.reply_to_message.media
    if "sticker" in str(typ).lower():
        m = m.sticker
        answer = f"""
Sticker
name: {m.set_name}
emoji: {m.emoji}
file ID: {m.file_id}
"""
    else:
        answer = m
    return await message.reply(answer)


@client.on_message(filter_startwith(lang["commands"]["list"]))
async def send_commands_bot(_, message):
    """Reply a command list"""
    answer = await commands_list()
    return await message.reply(answer)


@client.on_message(filter_startwith(lang["commands"]["stable"]))
async def check_bot_working(_, message):
    return await message.reply(lang["answers"]["stable"])


@client.on_message(filter_startwith(lang["commands"]["task"]))
async def change_interval(_, message):
    """not works yet.\nneed to restart the grow task"""
    global schedule_text, interval
    if message.from_user.id not in ADM_LIST:
        return
    if lang["commands"]["interval"] in message.text:
        try:
            text = int(message.text.split(" ", maxsplit=2)[2])
        except:
            text = 43200
        interval = text
        return await message.reply(f"{lang["answers"]["interval_change"]} {text}")
    elif lang["commands"]["text"] in message.text:
        try:
            text = message.text.split(" ", maxsplit=2)[2]
        except:
            text = "/grow"
        schedule_text = text
        return await message.reply(f"{lang["answers"]["text_change"]} {text}")


@client.on_message(filters.command(lang["commands"]["terminal"], comm_pref)) # тэрминал
async def bash_term(_, message):
    if message.from_user.id not in ADM_LIST:
        return await message.reply(lang["answers"]["unavaiable"])
    return await message.reply(terminal(message.text.split(" ", maxsplit=1)[1]))


@client.on_message(filters.command(lang["answers"]["exit"], comm_pref)) # вийти в окно
async def bash_term(_, message):
    if message.from_user.id not in ADM_LIST:
        return await message.reply(lang["answers"]["unavaiable"])
    exit()


# scheduler = AsyncIOScheduler() 
# scheduler.add_job(grow, "interval", seconds=interval)
# scheduler.add_job(download_map, "interval", seconds=60)
# scheduler.add_job(check_alerts, "interval", seconds=180)

# download_map()

# logging.debug("Alert bot launched")
# scheduler.start()
client.run()