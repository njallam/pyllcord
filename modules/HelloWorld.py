from datetime import datetime
from BaseModule import BaseModule


def my_message():
    return f"Hello World @ {datetime.now()}"


class Module(BaseModule):
    async def on_ready(self):
        channel = self.bot.get_channel(self.args["channel_id"])
        if "message_id" in self.state:
            message = channel.get_partial_message(self.state["message_id"])
            if message:
                await message.edit(content=my_message())
                return
        message = await channel.send(my_message())
        self.state["message_id"] = message.id
        self.save_state()
