from BaseModule import BaseModule


class Module(BaseModule):
    def __init__(self, client, args):
        self.client = client
        self.channel_id = args["channel_id"]

    async def on_ready(self):
        channel = self.client.get_channel(self.channel_id)
        await channel.send("Hello World")
