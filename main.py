import asyncio
import datetime
from lib.hunt import hunt
from lib.parser import conf
from discord.ext import commands
from discord.ext.commands import CommandNotFound

caught = 0
encounters = 0
start_time = 0

bot = commands.Bot(command_prefix=';', self_bot=True, help_command=None)

def footer(msg):
     embeds = msg.embeds
     for embed in embeds:
         footer=str(embed.footer)
         return footer

def description(msg):
     embeds = msg.embeds
     for embed in embeds:
         description=str(embed.description)
         return description

async def timer(after):
    await asyncio.sleep(conf.cooldowns.huntcooldown)
    await after.channel.send(";p")

async def log():
    current_time=datetime.datetime.now().replace(microsecond=0)
    time_elapsed=current_time - start_time
    print(f"Time Elapsed : {time_elapsed} | Encounters : {encounters} | Catches : {caught} |")

@bot.event
async def on_ready():
    global start_time

    user = await bot.fetch_user(conf.general.userid)
    channel = bot.get_channel(conf.general.channelid)

    await channel.send(";p")
    print(f"Started grinding as {user}.")
    start_time = datetime.datetime.now().replace(microsecond=0)

@bot.listen('on_message')
async def on_message(message):
    if message.author.id == 664508672713424926 and message.channel.id == conf.general.channelid:
        if "continue hunting!" in message.content:
            await asyncio.sleep(0.3)
            await message.channel.send(";p")

@bot.listen('on_message_edit')
async def on_message_edit(before, after):
    global caught
    if after.author.id == 664508672713424926 and after.channel.id == conf.general.channelid:
        asyncio.create_task(timer(after))

        if "caught" in description(after):
            caught += 1
        
        asyncio.create_task(log())

@bot.command()
async def p(ctx):
    global encounters
    if ctx.channel.id == conf.general.channelid:
        try:
            poke = await bot.wait_for('message', check = lambda m: m.author.id == 664508672713424926 and m.channel == ctx.channel, timeout=5)
        
        except asyncio.TimeoutError:
            await ctx.send(";p")
        
        else:
            if poke.embeds != []:
                if "found a wild" in description(poke):
                    encounters += 1

                    ball = hunt(footer(poke), description(poke))
                    await asyncio.sleep(conf.cooldowns.ballcooldown)
                    await ctx.send(ball)

                    try:
                        before, after = await bot.wait_for('message_edit', check = lambda b, m: b == poke, timeout=1.5)

                    except asyncio.TimeoutError:
                        await ctx.send(ball)
            
            else:
                if "please wait" in poke.content:
                    await asyncio.sleep(3)
                    await ctx.send(";p")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(conf.general.token)