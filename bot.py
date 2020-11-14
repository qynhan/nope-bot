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

#help command
client.remove_command("help")
@client.command()
async def help(ctx):
    await ctx.send('Here are the commands\n')
    await ctx.send("!join - join the game!\n"
                   "!quit - leave the game\n"
                   "!start - start the game once all players have joined\n"
                   "!table - display what is currently on the table. "
                   "this includes the number of card each player has in their hand\n"
                   "!hand - I will send you a dm with the cards in your hand\n"
                   "!play - play a card from your hand\n"
                   "!draw - draw a card from the table\n"
                   "!nope - shout NOPE!\n"
                   "!help - display this screen again\n"
                   "!howtoplay - display the instructions for the game")

client.run(TOKEN)
