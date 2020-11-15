import discord
from discord.ext import commands
from discord import File, Embed
from random import randint

from carddef import Card
from playerdef import Player
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

# check if the person who sent the command is a developer of the bot
def checkDev(ctx):
    return ctx.author.id == 467381662582308864 or ctx.author.id == 262273851310735361 or ctx.author.id == 270781353228763136 or ctx.author.id == 628390090514628618

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
        await game.showTable(ctx)

# join game
@client.command(aliases=["j"])
async def join(ctx):
    if game.status != "setup":
        await ctx.send('You cannot join the game after it has started')
    else:
        result = game.addPlayer(ctx.author)
        if result:
            await ctx.send(f'{ctx.author} joined the game!')

# quit game
@client.command(aliases=["q"])
async def quit(ctx):
    result = game.removePlayer(ctx.author)
    if result:
        await ctx.send(f'{ctx.author} left the game.')

# start game
@client.command(aliases=["s"])
async def start(ctx):
    # status must be setup
    if game.status == "setup":
        # number of players must be > 2
        if game.numPlayers < 3:
            await ctx.send('At least three players need to join the game before it can start!')
        else:
            game.generateDeck()
            game.currentCard = game.drawCard()
            game.status = "playing"
            await ctx.send("Ready to start!")
            await game.dealCards()
            for playerID in game.players:
                player = game.players[playerID]
                game.currentPlayer = player
                await player.sendHand("It's your turn! Here is your hand:")
                await game.showTable(ctx, showPlayers=False)
                await client.wait_for('message', check=game.validPlay)

# end game (for debugging only)
@client.command()
# only developers may run this command
@commands.check(checkDev)
async def end(ctx):
    # create a new game
    game.newGame()

    await ctx.send("Game ended.")

# see hand
@client.command(aliases=["h"])
async def hand(ctx):
    # do not show hand when they do not have cards yet
    if ctx.author.id not in game.players or game.status != "playing":
        await ctx.send("You have no cards.")
    else:
        await game.players[ctx.author.id].sendHand("Here is your hand:")

# tutorial youtube link command
@client.command(aliases=["tutorial", "howto", "htp"])
async def howtoplay(ctx):
    await ctx.send( "Here is the link for the tutorial of the game\n"
                    "https://www.youtube.com/watch?v=Xk0y7BSuJio")


@client.command()
async def play(ctx, *, message):
    print(game.validPlay(message))

# helper function for devs to automate tests
@client.command()
# only developers may run this command
@commands.check(checkDev)
async def test(ctx):
    await game.showTable(ctx, showPlayers=False)
    game.generateDeck()
    game.dealCards()

    for player in game.players.values():
        print(player.hand)
        print(player)
        for i in range(len(player.hand)):
            print(player.hand[i])
            await ctx.send(player.hand[i])
            await ctx.send(game.currentCard)

# adds author and two mentioned users to a game to make testing quicker
@client.command(aliases=['!'])
# only developers may run this command
@commands.check(checkDev)
async def setup(ctx, user1: discord.User, user2: discord.User):
    game.addPlayer(ctx.author)
    game.addPlayer(user1)
    game.addPlayer(user2)
    await table(ctx)

# run bot
client.run(TOKEN)
