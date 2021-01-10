import asyncio
import discord
import importlib.util
import json
from typing import Dict, List

from BaseModule import BaseModule

settings: Dict
with open("config.json") as f:
    settings = json.load(f)

client = discord.Client()

modules: List[BaseModule] = []

for m in settings["modules"]:
    spec = importlib.util.find_spec("modules." + m["name"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    modules.append(module.Module(client, m["args"]))


@client.event
async def on_ready():
    await asyncio.wait([m.on_ready() for m in modules])


client.run(settings["token"])
