import discord
import os
import requests
import logging
import pickle
from datetime import datetime, timezone
from discord.ext import commands,tasks

# getting the API keys from the environment variables
DTOKEN = os.getenv('DISCORD_TOKEN')
NTOKEN = os.getenv('NOTION_TOKEN')

# notion database id
DATABASE_ID = 'c0d85c444c84423aa78eb50b94410083'

# headers for the notion connection
headers = {
    "Authorization": "Bearer " + NTOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }

# a dict 
servers = dict()
# (guild id, notionpage) , string

# File path for storing the servers dictionary
SERVERS_FILE = 'servers.pkl'

# Load servers from file, if available
if os.path.isfile(SERVERS_FILE):
    with open(SERVERS_FILE, 'rb') as file:
        servers = pickle.load(file)
else:
    servers = {}

# discord bot settings, setting up the logging, & intents, NEEDS TO CHECK WHICH ARE NEEDED
handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} is now online')
    myLoop.start()
    # pages = get_pages()

    # for page in pages:
        # print(page)
        # page_id = page["id"]
        # props = page["properties"]
        # print(page_id)
        # print (props)
        # url = props["URL"]["title"][0]["text"]["content"]
        # title = props["Title"]["rich_text"][0]["text"]["content"]
        # published = props["Published"]["date"]["start"]
        # published = datetime.fromisoformat(published)
        # print("________________________")

        # print(url)
        # print(title)
        # print(published)
        

    #takenGuild = bot.get_guild(960593893970280468)
    #print(takenGuild.id)

    #for guild in bot.guilds:
    #    print(guild)
    #    print(guild.id)
    #myLoop.start()
    

@bot.command(pass_context=True)
async def start(ctx,arg1):
    # id = ctx.message.guild.id
    # takenGuild = bot.get_guild(id
    guildid = ctx.message.guild.id
    testSt = 'lmeow'
    entry = (int(guildid),str(arg1))
    servers.update({entry : testSt})
    # entry = ({961593893972340468:'9fda8eb2baa94a7bab8b784a7968e574'})
    # servers.update(entry)z
    # servers.update(entry)
    # replace these with ctx.message.guild 
    # print()
    await ctx.message.reply(content = "Starting the bot...")
   
    



@bot.command()
async def stop(ctx,arg1): # update to allow !stop [id]
    # remove this ctx.message.guild from the systems
    #                            [aka from the hot struct and logging] 
    await ctx.message.reply(content = "Removing your server from the bot...")
    entry = (ctx.message.guild.id,str(arg1))
    servers.pop(entry)
    await ctx.message.reply(content = "Removed!")


@tasks.loop(seconds = 10) # repeat after every x seconds
async def myLoop():
    print('tick')
    # print(servers)
    # activeServers = servers
    for server in servers:
        # print (server)
        guildx = bot.get_guild(server[0])
        events = await guildx.fetch_scheduled_events()
        for event in events:
            print(event)
            print(event.location)
            print(event.name)
            event_setup(str(event.start_time.astimezone(timezone.utc).isoformat()),server[1],event.location,event.name)
    
    # Save servers to file
    with open(SERVERS_FILE, 'wb') as file:
        pickle.dump(servers, file)
    print("tock")






    # guildx = bot.get_guild(960593893970280468)
    
    # events = []
    # events = await guildx.fetch_scheduled_events(True)
    # events = await guildx.fetch_scheduled_events()
    
    # print(events)
    # for event in events:
    #    print(event)
    





def create_event(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    # print(res.content) # uncomment for diaognostic
    return res


def event_setup(date_time,projectid,url,title):
    print(date_time)

    if event_exists(str(date_time), title, url):
        print("Event already exists in the Notion calendar.")
        return
    
    data = {
                    # ????? what is this lmeow
    "Date & Time": {'id': '%3DgE%3E', 'type': 'date', 'date': {'start': date_time, 'end': None, 'time_zone': None}},                   # need to decide if i want to pass whole object or just id-
    "Game/Team": {'id': 'A%40h%3F', 'type': 'rich_text', 'rich_text': [{'type': 'mention', 'mention': {'type': 'page', 'page': {'id': projectid}}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Untitled', 'href': 'https://www.notion.so/c7abdd593eab4678a9ccff2f58b2f8d6'}, {'type': 'text', 'text': {'content': ' ', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': ' ', 'href': None}]},
    "Location": {'id': 'x%3Bm%7C', 'type': 'url', 'url': url},
    'Title': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': title, 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': title, 'href': None}]}
    }
    create_event(data)

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)
    # print(data)
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

def event_exists(date_time, title, url):
    """
    Checks if an event with the given date and time, title, and URL already exists in the Notion calendar.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {
        "filter": {
            "and": [
                {
                    "property": "Date & Time",
                        "date": [{'start': date_time}]
                },
                {
                    "property": "Title",
                    "title": [
                        {
                            "text": {
                                "equals": title
                            }
                        }
                    ]
                },
                {
                    "property": "URL",
                    "url": {
                        "equals": url
                    }
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(data)

    return len(data.get("results", [])) > 0



# print(DTOKEN)
bot.run(DTOKEN,log_handler=handler)