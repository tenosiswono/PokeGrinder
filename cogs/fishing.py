import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from discord import InvalidData, HTTPException

from discord import (
    Message,
    Interaction,
    InteractionType,
    Button,
    SelectMenu,
    SelectOption,
    ActionRow,
)

rarities = [
    "Common",
    "Uncommon",
    "Super Rare",
    "Rare",
    "Event",
    "Full-odds",
    "Shiny",
    "Legendary",
]

colors = {
    "Common": "\033[1;34m",
    "Uncommon": "\033[1;36m",
    "Super Rare": "\033[1;33m",
    "Rare": "\033[1;31m",
    "Event": "\033[1;35m",
    "Full-odds": "\033[1;35m",
    "Shiny": "\033[1;35m",
    "Legendary": "\033[1;35m",
}

ball_strings = [
    "Pokeballs: 0",
    "Greatballs: 0",
    "Ultraballs: 0",
    "Masterballs: 0",
]


async def timer(command, timer) -> None:
    await asyncio.sleep(timer)
    await command()


class Fishing(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cast, self.catches, self.encounters = 0, 0, 0
        self.timer, self.delay, self.timeout, self.auto_buy = (
            client.timer_fish,
            client.delay,
            client.timeout,
            client.auto_buy,
        )
        self.auto_buy: dict

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction) -> None:
        
        if (
            interaction.type != InteractionType.application_command
            or interaction.name != "fish"
        ):
            return

        self.client.queue_ready = False
        current_time = datetime.now().replace(microsecond=0)

        print(
            f"Time Elapsed: {current_time - self.client.start_time} | "
            f"Cast: {self.cast} | "
            f"Encounters: {self.encounters} | "
            f"Catches: {self.catches}"
        )
        try:
            message: Message = await self.client.wait_for(
                "message",
                check=lambda message: interaction.channel.id == message.channel.id,
                timeout=self.timeout,
            )
            before, pull = await self.client.wait_for(
                "message_edit",
                check=lambda before, pull: before == message,
                timeout=self.timeout,
            )
            pull: Message
            print(pull.embeds[0].description)

        except asyncio.TimeoutError:
            now = datetime.today()
            next_run = now + timedelta(seconds=self.timer)
            self.client.queue.append([self.client.fish, next_run.timestamp()])
            self.client.queue_ready = True
            return
        
        try:
            if "wait" in message.content:
                await asyncio.sleep(2)
                await self.client.fish()
                return

            elif "answer the captcha below" in message.embeds[0].description:
                    print("\n\033[1;31m A captcha has appeared!!")
                    if self.client.config["captcha_solver"] != "True":
                        print(
                            "\033[1;33m Not solving the captcha as captcha solver is disabled!"
                        )
                        return
                    print("\033[1;33m Solving the captcha...")

                    image = message.embeds[0].image.url

                    dropdown: ActionRow = message.components[0]
                    menu: SelectMenu = dropdown.children[0]
                    options = menu.options

                    option: SelectOption = [
                        option
                        for option in options
                        if option.value == self.client.captcha_solver(image)
                    ][0]

                    try:
                        await menu.choose(option)

                    except InvalidData:
                        pass

                    return
        except IndexError:
            pass

        # wait fish
        self.cast += 1
        
        if 'bite' in pull.embeds[0].description:
            button: Button = pull.components[0].children[0]
            await button.click()
        else:
            now = datetime.today()
            next_run = now + timedelta(seconds=self.timer)
            self.client.queue.append([self.client.fish, next_run.timestamp()])
            self.client.queue_ready = True
            return

        self.encounters += 1
        try:
            before, catch = await self.client.wait_for(
                "message_edit",
                check=lambda before, catch: before == pull,
                timeout=self.timeout,
            )
            catch: Message

        except asyncio.TimeoutError:
            try:
                print("TimeoutError catch")
                pass

            except HTTPException:
                print("HTTPException catch")
                pass

            now = datetime.today()
            next_run = now + timedelta(seconds=self.timer)
            self.client.queue.append([self.client.fish, next_run.timestamp()])
            self.client.queue_ready = True
            return

        # pokemeow_message: Message = await self.client.wait_for(
        #     "message",
        #     check=lambda message: interaction.channel.id == message.channel.id,
        #     timeout=self.timeout,
        # )
        # print("pokemeow", pokemeow_message.content)
        # index = [
        #     index
        #     for index, rarity in enumerate(rarities)
        #     if rarity in pokemeow_message.content
        # ][0]

        # ball = list((self.client.config["rarities"]).values())[index]

        button_catch: Button = [
            component
            for component in catch.components[0].children
            if component.custom_id == "gb_fish"
        ][0]

        try:
            await asyncio.sleep(self.delay)
            await button_catch.click()

        except InvalidData:
            pass

        try:
            before, after = await self.client.wait_for(
                "message_edit",
                check=lambda before, after: before == catch,
                timeout=self.timeout,
            )
            after: Message

        except asyncio.TimeoutError:
            try:
                await button.click()

            except HTTPException:
                pass

            now = datetime.today()
            next_run = now + timedelta(seconds=self.timer)
            self.client.queue.append([self.client.fish, next_run.timestamp()])
            self.client.queue_ready = True
            return

        now = datetime.today()
        if "caught" in after.embeds[0].description:
            self.catches += 1

        if self.client.config["auto-buy"] != "True":
            return

        index = [
            index
            for index, string in enumerate(ball_strings)
            if string in (after.embeds[0].footer.text).replace(" :", ":")
        ]

        if index == []:
            return

        index = index[0]
        string = list(self.auto_buy.keys())[index]
        amount = list(self.auto_buy.values())[index]

        await asyncio.sleep(4 + self.delay)
        await self.client.shop_buy(item=f"{index + 1}", amount=amount)

        print(f"\n\033[1m Bought {amount} {string}!\n")

        next_run = now + timedelta(seconds=self.timer)
        self.client.queue.append([self.client.fish, next_run.timestamp()])
        self.client.queue_ready = True
    

    @commands.Cog.listener()
    async def on_message_edit(self, before, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or "continue playing!" not in message.content
        ):
            return

        print("\033[1;32m The captcha has been solved!\n")

        await asyncio.sleep(2)
        await self.client.fish()


    # @commands.Cog.listener()
    # async def on_message(self, message: Message) -> None:
    #     if message.content and "fishs" in message.content:

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Fishing(client))
