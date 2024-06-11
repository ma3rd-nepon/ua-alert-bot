from dotenv import dotenv_values

import subprocess
import jwt
import random
import requests
from PIL import Image

config = dotenv_values(".env")
regions = [(162, 116), (252, 132), (350, 150), (450, 125), (462, 168), (555, 92), (680, 142), (85, 243), (190, 260), (261, 261), 
            (270, 256), (380, 310), (533, 263), (647, 233), (788, 250), (930, 296), (565, 341), (703, 350), (862, 359), (460, 455), 
            (648, 477), (750, 470), (53, 358), (145, 344), (184, 363)]

headers = {
    "accept": "application/json",
    "Authorization": "f11822be:ca47c2aaa59fbb9d876a9909fdd8942d"
}

base_url = "api.ukrainealarm.com"


def gfc(name):
    try:
        return config[name]
    except KeyError:
        return "not found"
        
comm_pref = gfc("prefix")
prefix = "/"

def terminal(command):
    return subprocess.check_output(command, shell=True).decode("utf-8")


async def commands_list():
    comm = "cat"
    comm2 = "grep"
    commands = ""

    coms = terminal(f'cat "main.py" | grep ".on_message(filters.command"')
    for i in coms.split("\n"):
        res = ''
        if len(i.rstrip()) == 0:
            continue
        if "comm_pref" in i:
            res += comm_pref
        else:
            res += prefix
        res += i.split('"')[1]
        res += " -"
        if "#" in i:
            res += i.split('#')[1]
        else:
            res += f" "
        res += "\n"
        commands += res

    target = commands.split('\n')
    commands += f"\nВсего {len(target) - 1} команд."
    total_answer = commands

    return total_answer


def hash_name(message):
    return jwt_code(f"{message.id}{random.randint(1, 100)}{message.chat.id}")


def jwt_code(msg):
    key = "aoooa"
    alg = "HS512"
    text = {
        "text": msg
    }
    try:
        result = jwt.encode(text, key, algorithm=alg)
        return result[::-1]
    except Exception as e:
        return str(e)


def check_map():
    im = Image.open('other/map.png')
    rgb_im = im.convert('RGB')
    alerts = 0

    for i in regions:
        r, g, b = rgb_im.getpixel(i)
        if r == 221:
            alerts += 1
        else:
            pass
    return alerts >= 5


def check_regions():
    response = requests.get(f"{base_url}/api/v3/alerts", headers=headers).json()

    if len(response) >= 10:
        return [region["regionName"] for region in response]
    return False
