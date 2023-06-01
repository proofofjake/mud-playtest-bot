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
DATABASE_ID_OLD = 'c0d85c444c84423aa78eb50b94410083'
DATABASE_ID = '8ba759f42ab44f42adfa77677caea15a'

# headers for the notion connection
headers = {
    "Authorization": "Bearer " + NTOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }

# a dict 
servers = dict()
# (guild id, notionpageid) , string
events = dict()
# (date_time,title,projectid) , string
serversTBD = dict()
# events to be deleted

server_lock = False
# True is active

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
    entry = {(ctx.message.guild.id,str(arg1)):ctx.message.channel}
    print(entry)
    print(servers)
    serversTBD.update(entry)


@tasks.loop(seconds = 10) # repeat after every x seconds
async def myLoop():
    print('tick')
    print(servers)
    # activeServers = servers
    for server in servers:
        # print (server)
        guildx = bot.get_guild(server[0])
        tempevents = await guildx.fetch_scheduled_events()
        for event in tempevents:
            # print(event)
            # print(event.location)
            # print(event.name)
            event_setup(event.start_time.astimezone(timezone.utc).isoformat(),server[1],event.location,event.name)
            # print()
    
    # Save servers to file
    with open(SERVERS_FILE, 'wb') as file:
        pickle.dump(servers, file)


    check_deleted_servers()
    update_events(get_pages())

    print("tock")






    # guildx = bot.get_guild(960593893970280468)
    
    # events = []
    # events = await guildx.fetch_scheduled_events(True)
    # events = await guildx.fetch_scheduled_events()
    
    # print(events)
    # for event in events:
    #    print(event)
    


def check_deleted_servers():
    if len(serversTBD) == 0:
        return
    else:
        for server in serversTBD:
            servers.pop(server)
            print(server[0])


def create_event(data: dict):
    print("creating event!")
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    # print(res.content) # uncomment for diaognostic
    return res

def event_setup(date_time,projectid,url,title):
    if check_event_exists(date_time, title): #,projectid):
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
    return data
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

def check_event_exists(date_time, title): # , projectid):
    print('checking if exists.... ')
    date_time_parts = date_time.split("+")
    date_time = date_time_parts[0] + ".000+" + date_time_parts[1]   
    event_tuple = (str(date_time),title)#,projectid)
    return event_tuple in events

def update_events(pages):
    events_temp = pages['results']
    for event in events_temp:
        date_time = event['properties']['Date & Time']['date']['start']
        title = event['properties']['Title']['title'][0]['text']['content']
        # projectid = event['properties']['Game/Team']['rich_text'][0]['mention']['page']['id']

        event_tuple = (date_time,title) # ,projectid)

        events.update({event_tuple : True})

print(DTOKEN)
bot.run(DTOKEN,log_handler=handler)