import discord
from discord.ext import commands
from discord import File, Embed
from random import randint

from gamedef import Game
# create game
game = Game()

# get bot token
f = open("token.txt", "r")
TOKEN = f.read()
f.close()

# create bot
PREFIX = "!"
client = commands.Bot(command_prefix=PREFIX, case_insensitive=True)

# runs when the bot is first online
@client.event
async def on_ready():
    # set status
    await client.change_presence(activity=discord.Game('Nope!'))

    # make a new game
    game = Game()

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

# show game status
@client.command(aliases=["t"])
async def table(ctx):
    if game.numPlayers == 0:
        await ctx.send("No one has joined the game yet")
    else:
        if game.status == "setup":
            table = "The following people have joined the game:\n"
            for playerID in game.players:
                player = game.players[playerID]
                table += f'{player.user} ({player.user.display_name})\n'
            await ctx.send(table)
        else:
            await ctx.send("Table view for in-progress game not yet implemented") # todo

# join game
@client.command()
async def join(ctx):
    if game.status != "setup":
        await ctx.send('You cannot join the game after it has started')
    else:
        result = game.addPlayer(ctx.author)
        if result:
            await ctx.send(f'{ctx.author} joined the game!')

# quit game
@client.command()
async def quit(ctx):
    result = game.removePlayer(ctx.author)
    if result:
        await ctx.send(f'{ctx.author} left the game.')

# tutorial youtube link command
@client.command()
async def howtoplay(ctx):
    await ctx.send( "Here is the link for the tutorial of the game\n"
                    "https://www.youtube.com/watch?v=Xk0y7BSuJio")

# run bot
client.run(TOKEN)
