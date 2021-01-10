class BaseModule:
    def __init__(self, client, config, save_state):
        self.client = client
        self.args = config["args"]
        self.state = config["state"]
        self.save_state = save_state

    async def on_ready(self):
        pass
