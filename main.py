import discord
import json
import guideMaker

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("/guide"):
        await message.channel.send(message.content.split(" ")[1:])
        await message.channel.send(guideMaker.generate(message.content.split(" ")[1:]))
    else:
        await message.channel.send(message.author.name + " said: " + message.content)

with open("config.json") as jsonFile:
    config = json.load(jsonFile)

client.run(config["BOT_API_KEY"])