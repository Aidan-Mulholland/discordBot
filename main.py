import discord
import json



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(message.author.name + " said: " + message.content)

with open("config.json") as jsonFile:
    config = json.load(jsonFile)    
client.run(config["BOT_API_KEY"])