import discord
import os
import requests
import logging
from datetime import datetime, timezone
from discord.ext import commands,tasks




DTOKEN = os.getenv('DISCORD_TOKEN')
NTOKEN = os.getenv('NOTION_TOKEN')

DATABASE_ID = ''

headers = {
    "Authorization": "Bearer " + NTOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }



handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} is now online')

    #takenGuild = bot.get_guild(960593893970280468)
    #print(takenGuild.id)

    #for guild in bot.guilds:
    #    print(guild)
    #    print(guild.id)
    #myLoop.start()
    

@bot.command(pass_context=True)
async def start(ctx):
    id = ctx.message.guild.id
    takenGuild = bot.get_guild(id)
    print(takenGuild.id)
    await ctx.message.reply(content = "Starting the bot...")



@bot.command()
async def stop(ctx):
    # remove this ctx.message.guild from the systems 
    await ctx.message.reply(content = "Stopping the bot...")


@tasks.loop(seconds = 30) # repeat after every x seconds
async def myLoop():
    guildx = bot.get_guild(960593893970280468)
    print('tick')
    events = []
    events = await guildx.fetch_scheduled_events(True)
    # events = await fetch_scheduled_events(True)
    print(events)
    for event in events:
        print(event)





def create_event(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res


def event_setup(title,description):
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    data = {
        "URL": {"title": [{"text": {"content": description}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Published": {"date": {"start": published_date, "end": None}}
    }
    create_event(data)


print(DTOKEN)
bot.run(DTOKEN,log_handler=handler)