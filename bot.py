import discord
import importlib.util
import json
from collections import defaultdict
from discord.ext import commands

config = open("config.json", "r+")
settings = json.load(config)

bot = commands.Bot(command_prefix=">")
modules = []


def save_state():
    config.seek(0)
    json.dump(settings, config, indent=2)
    config.truncate()


for m in settings["modules"]:
    spec = importlib.util.find_spec("modules." + m["name"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if "state" not in m:
        m["state"] = {}
    modules.append(module.Module(bot, m, save_state))

print(discord.utils.oauth_url(settings["client_id"]))


bot.run(settings["token"])
