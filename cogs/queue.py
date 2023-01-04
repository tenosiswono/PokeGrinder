from discord.ext import tasks, commands
from discord.channel import TextChannel
import asyncio
import time
def takeSecond(elem):
    return elem[1]

def write_logs(status):
    with open('logs.txt', 'a') as filetowrite:
        filetowrite.write(status)
class Queue(commands.Cog):
    def __init__(self, client) -> None:
        print('queue runner init')
        self.client: commands.Bot = client
        self.client.queue = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.runner.start()

    def cog_unload(self):
        self.client.queue = []
        self.runner.stop()

    @tasks.loop(seconds=4.0)
    async def runner(self):
        cur_ts = time.time()
        self.client.queue.sort(key=takeSecond)
        if(len(self.client.queue) > 0) and self.client.queue_ready:
            next_task_check = self.client.queue[0]
            command = next_task_check[0]
            exec_ts = next_task_check[1]
            if exec_ts < cur_ts:
                self.client.queue_ready = False
                self.client.queue.pop(0)
                await asyncio.sleep(2)
                await command()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Queue(client))
