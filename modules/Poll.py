import discord
import re
from BaseModule import BaseModule

p = re.compile("poll:", re.I)


class Module(BaseModule):
    async def on_message(self, message: discord.Message):
        if p.match(message.content):
            await message.add_reaction("👍")
            await message.add_reaction("👎")
