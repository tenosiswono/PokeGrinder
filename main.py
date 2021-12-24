print("Importing Modules...")

import asyncio
import datetime
from lib.hunt import hunt
from lib.parser import conf
from playsound import playsound
from discord.ext import commands
from lib.autobuy import get_balls
from lib.captcha import anticaptcha
from discord.ext.commands import CommandNotFound

print("Initialising, this may take some time depending on your hardware.")

caught = 0
encounters = 0
solved = 0
start_time = 0
hatched = 0
notification = r'lib/assets/notification.mp3'

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

async def notify():
    if conf.general.captcha_notifier == 'enable':
        repeat = 0
        while repeat <= 3:
            playsound(notification)
            repeat += 1

async def timer(after):
    await asyncio.sleep(conf.cooldowns.huntcooldown)
    await after.channel.send(";p")

async def log():
    current_time=datetime.datetime.now().replace(microsecond=0)
    time_elapsed=current_time - start_time
    print(f"Time Elapsed : {time_elapsed} | Encounters : {encounters} | Catches : {caught} | Captchas Solved : {solved} | Eggs Hatched : {hatched}")

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
    global solved
    if message.author.id == 664508672713424926 and message.channel.id == conf.general.channelid:
        if "continue hunting!" in message.content:
            await asyncio.sleep(1)
            await message.channel.send(";p")
        
        elif "You have **10** attempts to answer the captcha." in message.content:
                if len(message.attachments) != 0:
                    if conf.general.captcha_solver == "enable":
                        try:
                            answer = await anticaptcha(image = message.attachments[0])
                            print(f"Solved the captcha, expected answer is {answer}.")
                            await message.channel.send(answer)
                        
                        except:
                            print("Unable to solve Captcha!")
                            asyncio.create_task(notify())
                        
                        else:
                            try:
                                result = await bot.wait_for('message', check = lambda m: m.author == message.author and m.channel == message.channel, timeout=10)

                            except:
                                pass

                            else:
                                if 'continue hunting!' in result.content:
                                    print("The answer was correct!")
                                    solved += 1
                                
                                else:
                                    print("The answer was inccorect!")
                                    asyncio.create_task(notify())
                    
                    else:
                        asyncio.create_task(notify())
        
        elif 'ready to hatch!' in message.content:
            if conf.general.eggs != 'enable':
                return

            await asyncio.sleep(3.5)
            await message.channel.send(';egg hatch')

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
                        if conf.general.autobuy == 'enable':
                            await asyncio.sleep(3.5)

                            balls = await get_balls(footer(after))

                            if balls != None:
                                await ctx.send(balls)
            
            else:
                if "please wait" in poke.content:
                    await asyncio.sleep(3)
                    await ctx.send(";p")

@bot.command()
async def egg(ctx, action):
    if conf.general.eggs != 'enable':
        return

    global hatched
    if ctx.channel.id == conf.general.channelid:
        if action == 'hatch':
            try:
                response = await bot.wait_for('message', check = lambda m: m.author.id == 664508672713424926 and m.channel == ctx.channel, timeout=5)
        
            except asyncio.TimeoutError:
                await asyncio.sleep(3)
                await ctx.send(';egg hatch')
        
            else:
                if 'just hatched a' in response.content:
                    print("Hatched an egg!")
                    hatched += 1

                    await asyncio.sleep(8)
                    await ctx.send(';egg hold')
        
        elif action == 'hold':
            try:
                response = await bot.wait_for('message', check = lambda m: m.author.id == 664508672713424926 and m.channel == ctx.channel, timeout=5)
        
            except asyncio.TimeoutError:
                await asyncio.sleep(3)
                await ctx.send(';egg hold')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(conf.general.token)