import discord
from discord.ext import commands
import json

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def guide(ctx, *args):
    embed=discord.Embed(
        title="Guide",
        description="Sylas Items",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://images2.minutemediacdn.com/image/upload/c_fill,w_912,ar_16:9,f_auto,q_auto,g_auto/shape/cover/sport/lol--f23c5f332072d98de640cdfb5a3b4980.jpg")
    with open("items.json") as itemsJSON:
        items = json.load(itemsJSON)
        for i in args:
            embed.set_image(url=items[i])
    await ctx.send(embed=embed)

with open("config.json") as jsonFile:
    config = json.load(jsonFile)

bot.run(config["BOT_API_KEY"])