import asyncio
from discord.ext import commands
from discord import InvalidData, HTTPException
import sys
from random import randrange, uniform
import difflib
import os
import re
import time
from datetime import datetime, timedelta

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

rarities_short = [
    "C",
    "U",
    "S",
    "R",
    "E",
    "FO",
    "SH",
    "L",
]

cheaps = [
    "Latios",
    "Latias",
    "Suicune",
    "Kyogre",
    "Entei",
    "Zygarde",
    "Ho-oh",
    "Moltres",
    "Zapdos",
    "Raikou"
]

hunt_targets = [
    "Meowth",
    "Natu",
    "Azurill"
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

def update_status(status):
    with open('status.txt', 'w') as filetowrite:
        filetowrite.write(status)
def update_time(status):
    with open('time.txt', 'w') as filetowrite:
        filetowrite.write(status)
def update_details(status):
    with open('details.txt', 'w') as filetowrite:
        filetowrite.write(status)

def get_value(n):
    return n.value

async def timer(command, timer) -> None:
    await asyncio.sleep(randrange(10, timer))
    await command()

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


async def solve_captcha(self, message, interaction, index):
    if index > 3:
        notify(title    = '‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️',
            subtitle = f'Attempt {index} captcha solver FAILED',
            message  = 'PLEASE DO MANUAL CHECK')
        sys.exit(43)
    update_status('❓❓Solving the captcha❓❓')
    print("\033[1;33m Solving the captcha...")
    image = message.embeds[0].image.url

    dropdown: ActionRow = message.components[0]
    menu: SelectMenu = dropdown.children[0]
    options = menu.options
    solver_result = self.client.captcha_solver(image)
    option_values = map(get_value, options)
    options_matches = difflib.get_close_matches(solver_result, option_values)
    print(f"\033[1;33m Solver: {solver_result} Possible matches: {options_matches}")
    try:
        option: SelectOption = [
            option
            for option in options
            if option.value == options_matches[0]
        ][0]

        res =  menu.choose(option)
        update_status('✅✅A captcha has been solved✅✅')
        notify(title    = '✅✅A captcha has been solved✅✅',
            subtitle = 'Solving the captcha',
            message  = f'result: {options_matches[0]}')

        await res
        
    except IndexError:
        update_status('‼‼captcha solver FAILED‼‼')
        notify(title    = '‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️',
            subtitle = f'Attempt {index + 1} captcha solver FAILED',
            message  = f'Value: {options_matches[0]}')
    except InvalidData:
        return

class Hunting(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.catches, self.encounters = 0, 0
        self.timer, self.delay, self.timeout, self.auto_buy = (
            client.timer,
            client.delay,
            client.timeout,
            client.auto_buy,
        )
        self.auto_buy: dict
        self.catch_rarity_list = {
            "Common": 0,
            "Uncommon": 0,
            "Super Rare": 0,
            "Rare": 0,
            "Event": 0,
            "Full-odds": 0,
            "Shiny": 0,
            "Legendary": 0,
        }

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction) -> None:
        if (
            interaction.type != InteractionType.application_command
            or interaction.name != "pokemon"
        ):
            return
        
        try:
            message: Message = await self.client.wait_for(
                "message",
                check=lambda message: interaction.channel.id == message.channel.id,
                timeout=self.timeout,
            )

        except asyncio.TimeoutError:
            # now = datetime.today()
            # next_run = now + timedelta(seconds=15)
            # self.client.queue.append([self.client.pokemon, next_run.timestamp()])
            # self.client.queue_ready = True
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return
        try:
            if "You must wait until" in message.content:
                sys.exit(43)
            
            elif "wait" in message.content:
                await asyncio.sleep(2)
                await self.client.pokemon()
                # now = datetime.today()
                # next_run = now + timedelta(seconds=2)
                # self.client.queue.append([self.client.pokemon, next_run.timestamp()])
                # self.client.queue_ready = True
                return

            elif "answer the captcha below" in message.embeds[0].description:
                print("\n\033[1;31m A captcha has appeared!!")
                if self.client.config["captcha_solver"] != "True":
                    print(
                        "\033[1;33m Not solving the captcha as captcha solver is disabled!"
                    )
                    return
                
                await solve_captcha(self, message, interaction, 0)

                return
        except IndexError:
            pass

        self.encounters += 1
        try:
            index = [
                index
                for index, rarity in enumerate(rarities)
                if rarity in message.embeds[0].footer.text
            ][0]
            pattern = r"\b[>] [*][*].*?[*][*]!<:"
            pokemon_name = re.sub('[>*! <:]', '', re.findall(pattern, message.content)[0])
            if ':held_item:' in message.embeds[0].description:
                # override common and uncomon as rare, rare as super rare
                if index == 0 or index == 1:
                    index = 3
                elif index == 3:
                    index = 2
            # override cheap legendary
            index_cheap = [
                index
                for index, cheap in enumerate(cheaps)
                if cheap == pokemon_name
            ]
            if len(index_cheap) > 0:
                index = 2

            # override hunt target to rare
            index_hunt_target = [
                index
                for index, hunt_target in enumerate(hunt_targets)
                if hunt_target == pokemon_name
            ]
            if len(index_hunt_target) > 0:
                index = 3

            ball = list((self.client.config["rarities"]).values())[index]

            button: Button = [
                component
                for component in message.components[0].children
                if component.custom_id == ball
            ][0]

            try:
                await asyncio.sleep(uniform(0.5, self.delay))
                await button.click()

            except InvalidData:
                pass
        except IndexError:
            # now = datetime.today()
            # next_run = now + timedelta(seconds=15)
            # self.client.queue.append([self.client.pokemon, next_run.timestamp()])
            # self.client.queue_ready = True
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        try:
            before, after = await self.client.wait_for(
                "message_edit",
                check=lambda before, after: before == message,
                timeout=self.timeout,
            )
            after: Message

        except asyncio.TimeoutError:
            try:
                await button.click()

            except HTTPException:
                pass

            # now = datetime.today()
            # next_run = now + timedelta(seconds=15)
            # self.client.queue.append([self.client.pokemon, next_run.timestamp()])
            # self.client.queue_ready = True
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return
        
        # now = datetime.today()
        # next_run = now + timedelta(seconds=15)
        # self.client.queue.append([self.client.pokemon, next_run.timestamp()])
        # self.client.queue_ready = True
        status = "❌"
        if "caught" in after.embeds[0].description:
            self.catches += 1
            self.catch_rarity_list[rarities[index]] += 1
            status = "✅"
        current_time = datetime.now().replace(microsecond=0)

        print(
            f"{list(colors.values())[index]}{rarities_short[index]} - {pokemon_name} \033[1;0m"
            f"| {status} | "
            f"Σ: {self.encounters} | "
            f"n: {self.catches}"
        )
        update_time(f"Time Elapsed: {current_time - self.client.start_time}")
        update_details(
            f"C: {self.catch_rarity_list['Common']} | "
            f"U: {self.catch_rarity_list['Uncommon']} | "
            f"R: {self.catch_rarity_list['Rare']} | "
            f"S: {self.catch_rarity_list['Super Rare']} | "
            f"E: {self.catch_rarity_list['Event']} | "
            f"FO: {self.catch_rarity_list['Full-odds']} | "
            f"SH: {self.catch_rarity_list['Shiny']} | "
            f"L: {self.catch_rarity_list['Legendary']}"
        )
        update_status(
            f"{rarities_short[index]} - {pokemon_name} {status} | "
            f"Σ: {self.encounters} | "
            f"n: {self.catches}"
        )

        if self.client.config["auto-buy"] != "True":
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        index = [
            index
            for index, string in enumerate(ball_strings)
            if string in (after.embeds[0].footer.text).replace(" :", ":")
        ]

        if index == []:
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        index = index[0]
        string = list(self.auto_buy.keys())[index]
        amount = list(self.auto_buy.values())[index]
        if amount > 0:
            await asyncio.sleep(self.delay)
            await self.client.shop_buy(item=f"{index + 1}", amount=amount)

            print(f"\n\033[1m Bought {amount} {string}!\n")

        asyncio.create_task(timer(self.client.pokemon, self.timer))

    @commands.Cog.listener()
    async def on_message_edit(self, before, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or "continue playing!" not in message.content
        ):
            return

        print("\033[1;32m The captcha has been solved!\n")

        await asyncio.sleep(randrange(2, 4))
        await self.client.pokemon()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Hunting(client))
