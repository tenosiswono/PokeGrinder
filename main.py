import json
import asyncio
from discord.ext import commands

config = open(r"config.json")
config = json.load(config)

client = commands.Bot(command_prefix="!@#$%^&*())(*&^%$#@!")
client.config = config

client.token, client.channel = config["token"], config["channel"]
client.timer, client.delay, client.timeout, client.auto_buy, client.timer_fish = (
    config["timer"],
    config["delay"],
    config["timeout"],
    config["auto_buy"],
    config["timer_fish"],
)

client.queue = []
client.queue_ready = True

if config["captcha_solver"] == "True":
    from modules.captcha_solver import solve

    client.captcha_solver = solve


async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    # await client.load_extension("cogs.queue")
    await client.load_extension("cogs.hunting")
    await client.load_extension("cogs.egg")
    # await client.load_extension("cogs.fishing")

loop = asyncio.get_event_loop()
loop.run_until_complete(load_cogs())
client.run(client.token)
