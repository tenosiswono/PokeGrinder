import os
from datetime import datetime, timedelta
from discord.ext import commands
from discord.channel import TextChannel
import asyncio


class Startup(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

        print("PokeGrinder is ready to grind!")
        print(f"Username: {self.client.user.name}" f"#{self.client.user.discriminator}")

        coolest_ascii_font = """\033[1;33m
       __________       __            ________      .__            .___            
       \______   \____ |  | __ ____  /  _____/______|__| ____    __| _/___________ 
        |     ___/  _ \|  |/ // __ \/   \  __\_  __ \  |/    \  / __ |/ __ \_  __ \\
        |    |  (  <_> )    <\  ___/\    \_\  \  | \/  |   |  \/ /_/ \  ___/|  | \/
        |____|   \____/|__|_  \\___  >\______  /__|  |__|___|  /\____ |\___  >__|   
                            \/    \/        \/              \/      \/    \/       
        """
        print(coolest_ascii_font)

        self.client.start_time = datetime.now().replace(microsecond=0)
        channel: TextChannel = self.client.get_channel(self.client.channel)

        commands = [
            commands
            async for commands in channel.slash_commands(
                command_ids=[1015311085441654824, 1015311085517156481, 1015311084812501026, 1015311084594405485]
            )
        ]

        await commands[3].children[0]()
        await asyncio.sleep(20)
        await commands[0]()
        self.client.queue_ready = True
        self.client.egg_hatch = commands[3].children[2]
        self.client.egg_hold = commands[3].children[1]
        self.client.pokemon = commands[0]
        self.client.shop_buy = commands[1].children[1]
        self.client.fish = commands[2].children[2]
        # now = datetime.today()
        # next_run = now + timedelta(seconds=21)
        # self.client.queue.append([self.client.fish, next_run.timestamp()])
        # await self.client.fish()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Startup(client))
