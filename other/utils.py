from dotenv import dotenv_values

import subprocess
import jwt
import random

config = dotenv_values(".env")


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