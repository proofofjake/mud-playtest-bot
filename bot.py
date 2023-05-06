import discord
import os
from discord.ext import commands,tasks
import logging



TOKEN = os.getenv('DISCORD_TOKEN')

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












TOKEN = 'MTEwNDE4NjQyODAwODY5Nzg1Ng.GazlL9.pL4aKoVGpoPKUzfxZ4MhgyLBsiF8nJJLj5ZZg8'

print(TOKEN)
bot.run(TOKEN,log_handler=handler)