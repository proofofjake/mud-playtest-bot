import os
import discord
from discord.ext import tasks
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DTOKEN = os.getenv('DISCORD_TOKEN')
bot_token = DTOKEN
channel_id = 148853766450315264  # your discord user id (right click on your name and copy ID)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if event.src_path == './discord.log':
            with open(event.src_path, 'r') as file:
                if 'crash' in file.read():
                    self.send_alert(event.src_path)

    async def send_alert(self, path):
        channel = bot.get_channel(channel_id)
        await channel.send(f'ALERT: The log file {path} contains a crash!')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

bot.run(bot_token)