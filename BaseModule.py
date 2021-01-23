from discord.ext import commands
from typing import Callable


class BaseModule:
    def __init__(
        self,
        bot: commands.Bot,
        config: dict[str, dict[str]],
        save_state: Callable[[], None],
    ):
        self.bot = bot
        self.args = config["args"]
        self.state = config["state"]
        self.save_state = save_state

        for f in dir(self):
            if f.startswith("on"):
                bot.add_listener(getattr(self, f))
