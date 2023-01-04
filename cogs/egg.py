import asyncio
from discord.ext import commands

from discord import (
    Message,
)

class Egg(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
        ):
            return

        if message.content and "your egg is ready to hatch" in message.content and self.is_egg_held == True and self.egg_held_counter > 0:
            self.client.queue_ready = False
            print("\033[1;32m Egg Ready to hatch!")
            await asyncio.sleep(3)
            await self.client.egg_hatch()
            await asyncio.sleep(8)
            await self.client.egg_hold()
            await asyncio.sleep(3)
            self.egg_held_counter -= 1
            print("\033[1;32m Egg hatched! and holded")
            print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")
            self.client.queue_ready = True
            return

        try:
            if (
                message.embeds and "<:poke_egg:685341229587890208> Your Eggs:" in message.embeds[0].description
            ): 
                self.client.queue_ready = False
                message_line_containing_number = message.embeds[0].description.splitlines()[0]
                egg_number = int(message_line_containing_number.replace("<:poke_egg:685341229587890208> Your Eggs: ", ""))
                self.egg_held_counter = egg_number
                self.is_egg_held = "You ARE holding an egg!" in message.embeds[0].description or "READY TO HATCH!" in message.embeds[0].description

                print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")

                if (
                    "READY TO HATCH!" in message.embeds[0].description
                ):
                    print("\033[1;32m Egg Ready to hatch!")
                    await asyncio.sleep(8)
                    await self.client.egg_hatch()
                    await asyncio.sleep(8)
                    await self.client.egg_hold()
                    await asyncio.sleep(3)
                    self.egg_held_counter -= 1
                    print("\033[1;32m Egg holded!")
                    print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")
                    self.client.queue_ready = True
                    return

                if (self.is_egg_held == False):
                    await asyncio.sleep(8)
                    await self.client.egg_hold()
                    await asyncio.sleep(3)
                    self.egg_held_counter -= 1
                    print("\033[1;32m Holding Egg")
                    self.client.queue_ready = True
                    return
                
                self.client.queue_ready = True
        except:
            self.client.queue_ready = True
            pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Egg(client))
