import discord
from datetime import datetime
from zoneinfo import ZoneInfo

import utils
from BaseModule import BaseModule


class Module(BaseModule):
    async def get_embed(self):
        data = await utils.get_json(
            f"https://xt.streamlabs.com/api/v5/twitch-extensions/countdown/{self.args['streamlabs_id']}/settings"
        )
        self.last_updated = datetime.now()
        description = None
        if data["disableUntil"]:
            time = data["disableUntil"]
            if time.endswith("Z"):
                time = time[:-1] + "+00:00"
            time = (
                datetime.fromisoformat(time)
                .astimezone(tz=ZoneInfo(data["timezone"]))
                .strftime("%d %B")
            )

            description = f"NOTE: No streams scheduled until after {time}."
        embed = discord.Embed(
            title="Stream Schedule",
            description=description,
            timestamp=self.last_updated,
        )
        embed.set_footer(text=f"{data['timezone']} (UTC{data['timezoneOffset']:+d})")
        for day in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            if data["enabled"][day]:
                times = "\n".join(map(lambda t: f"{t['HH']}:{t['mm']}", data[day]))
                if times:
                    embed.add_field(name=day.title(), value=times)
        return embed

    async def edit_or_send_message(self):
        channel = self.bot.get_channel(self.args["channel_id"])
        if "message_id" in self.state:
            message = channel.get_partial_message(self.state["message_id"])
            if message:
                await message.edit(embed=await self.get_embed())
                await message.add_reaction("🔄")
                return
        message = await channel.send(embed=await self.get_embed())
        await message.add_reaction("🔄")
        self.state["message_id"] = message.id
        self.save_state()

    async def on_ready(self):
        await self.edit_or_send_message()

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if (
            payload.member.id != self.bot.user.id
            and payload.message_id == self.state["message_id"]
            and payload.emoji.name == "🔄"
        ):
            await self.edit_or_send_message()
