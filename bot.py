import discord
from discord.ext import commands
from discord import File, Embed
from random import randint


f = open("token.txt", "r")
TOKEN = f.read()
f.close()
client = commands.Bot(command_prefix="!", case_insensitive=True)


# runs when the bot is first online
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Nope!'))
    print("ready!")

# common ping command for connection testing
@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

client.run(TOKEN)