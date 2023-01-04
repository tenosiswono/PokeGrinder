
# import difflib

# ans = '890924'
# options = ['89293',
# '86802',
# '87115',
# '83263',
# '82962',
# '82792',
# '89092',
# '89091',
# '88092',
# '89192']
# options_matches = difflib.get_close_matches(ans, options)

# print(options_matches)
# ## ['89092', '89192', '89091']

# import re
# s = '**ten** found a wild  <:189_:722265188371529809> **Jumpluff**!<:pokeball_locked:996646917104742512><:greatball_unlocked:996740567402811433><:ultraball_locked:996741024363843665><:premierball_locked:996741417504346112><:masterball_locked:996741226172788810><:beastball_locked:996741658072842240>'
# pattern = r"\b[>] [*][*].*?[*][*]!<:"
# print(re.sub('[>*! ]', '', re.findall(pattern, s)[0]))
# from datetime import datetime, timedelta

# now = datetime.today()
# print(now)  # 👉️ 2022-12-17 12:56:10.092082

# result = now + timedelta(seconds=15)
# print(result.timestamp())  # 👉️ 2022-12-17 12:56:25.092082

from discord.ext import tasks
import asyncio
import json
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
    # await client.load_extension("cogs.startup")
    await client.load_extension("cogs.queue")
    # await client.load_extension("cogs.hunting")
    # await client.load_extension("cogs.fishing")

loop = asyncio.get_event_loop()
loop.run_until_complete(load_cogs())
client.run(client.token)
