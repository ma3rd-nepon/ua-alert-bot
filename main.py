from pyrogram import *
from pyrogram.errors import MessageTooLong
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from other.utils import *
from io import BytesIO

import requests

client = Client(name=gfc("name"),
                api_id=gfc("api_id"),
                api_hash=gfc("api_hash"),
                bot_token=gfc("bot_token"))

prefix = "/"
comm_pref = gfc("prefix")
interval = 43200
schedule_text = "/grow"
image = "other/map.png"
ADM_LIST = [1242755674]
main_chat = -1001972773156
alert = False


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
    img = requests.get("https://alerts.com.ua/map.png").content
    with open("other/map.png", "wb+") as file:
        file.write(img)
    print("new map downloaded")


async def check_alerts():
    if check_regions() and not alert:
        file_id = "CAACAgIAAxkBAAEMSHlmZvlpuLQ-rNav_OWTXkOMWLQnzgACyB8AAoxioUroPLLHdVTODjUE"
        alert = True

        await client.send_sticker(chat_id=main_chat, sticker=file_id)

    elif alert and not check_regions():
        file_id = "CAACAgIAAxkBAAEMSHtmZvmBzqSsB-nN4Y1JZzsBc7c2XQACZR4AAkqJoUp24XobBmy_JDUE"

        alert = False

        await client.send_sticker(chat_id=main_chat, sticker=file_id)


@client.on_message(filters.command("start", prefix)) # старт
async def greetings(_, message):
    return await message.reply(f"Вітаю {message.from_user.first_name}! я бот для відправки стікерів під час алерту")


@client.on_message(filters.command("map", prefix)) # карта тревог
async def send_map_alerts(_, message):
    return await client.send_photo(chat_id=message.chat.id, photo=image)


@client.on_message(filters.command("sticker", prefix)) # сенд стикер через филе ид
async def send_sticker_by_file_id(_, message):
    try:
        file_id = message.text.split(" ", maxsplit=1)[1]
    except:
        file_id = "CAACAgIAAxkBAAMPZmWivOBjcNMsqZQ_gBH1j3eMYvEAAkciAALYQahKjCShe_CVt-seBA"
    return await client.send_sticker(chat_id=message.chat.id, sticker=file_id)


@client.on_message(filters.command("message", comm_pref)) # мессаге жсон
async def send_msg_json(_, message):
    try:
        text = "```json" + str(message) + "```"
        return await message.reply(text)
    except MessageTooLong:
        filename = hash_name(message)
        with open(f"messages/{filename}.txt", "w+") as file:
            file.write(str(message))
        return await client.send_document(chat_id=message.chat.id, document=f"messages/{filename}.txt")


@client.on_message(filters.command("file_id", prefix)) # сенд филе ид
async def get_file_id(_, message):
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


@client.on_message(filter_startwith("команды")) # команды ало
async def send_commands_bot(_, message):
    answer = await commands_list()
    return await message.reply(answer)


@client.on_message(filter_startwith("хрюка"))
async def check_bot_working(_, message):
    return await message.reply("нахрюкиваю у джакузи")


@client.on_message(filter_startwith("schedule")) # ижменение данных таска
async def change_interval(_, message):
    """not works yet.\nneed to restart the grow task"""
    global schedule_text, interval
    if message.from_user.id != 1242755674:
        return
    if "интервал" in message.text:
        try:
            text = int(message.text.split(" ", maxsplit=2)[2])
        except:
            text = 43200
        interval = text
        return await message.reply(f"interval grow changed to {text}")
    elif "текст" in message.text:
        try:
            text = message.text.split(" ", maxsplit=2)[2]
        except:
            text = "/grow"
        schedule_text = text
        return await message.reply(f"text changed to {text}")


@client.on_message(filters.command("bash", comm_pref)) # тэрминал
async def bash_term(_, message):
    if message.from_user.id not in ADM_LIST:
        return await message.reply("нэээээд")
    return await message.reply(terminal(message.text.split(" ", maxsplit=1)[1]))


@client.on_message(filters.command("exit", comm_pref)) # вийти в окно
async def bash_term(_, message):
    if message.from_user.id not in ADM_LIST:
        return await message.reply("нэээээд")
    exit()


scheduler = AsyncIOScheduler() 
# scheduler.add_job(grow, "interval", seconds=interval)
scheduler.add_job(download_map, "interval", seconds=60)
# scheduler.add_job(check_alerts, "interval", seconds=180)

download_map()

print("alert bot started work")
scheduler.start()
client.run()