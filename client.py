import asyncio
import discord
import importlib.util
import json

config = open("config.json", "r+")
settings = json.load(config)

client = discord.Client()

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
    modules.append(module.Module(client, m, save_state))


@client.event
async def on_ready():
    await asyncio.wait([m.on_ready() for m in modules])


client.run(settings["token"])
