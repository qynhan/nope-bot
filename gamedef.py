import discord
from discord import Embed
import random
from playerdef import Player
from carddef import Card

class Game:
    # constructor
    def __init__(self):
        self.players = {}
        self.numPlayers = 0
        self.status = "setup"
        self.deck = []
        self.drawPile = []
        self.discardPile = []
        self.currentCard = None
        self.currentPlayer = None
        self.message = None

    # add player to game, takes in user who ran the join command
    def addPlayer(self, user : discord.User):
        # do not add someone who already joined
        playerAdded = False
        if user.id not in self.players:
            self.players[user.id] = (Player(user))
            self.numPlayers += 1
            playerAdded = True

        return playerAdded

    # remove player from game, takes in user who ran the quit command
    def removePlayer(self, user : discord.User):
        # find player in list and remove, if they have not joined yet they will not be removed
        playerQuit = False
        if user.id in self.players:
            self.players.pop(user.id)
            self.numPlayers -= 1
            playerQuit = True

        return playerQuit

    # clear current values to set up for a new game
    def newGame(self):
        self.players = {}
        self.numPlayers = 0
        self.status = "setup"
        self.deck = []
        self.drawPile = []
        self.discardPile = []
        self.currentCard = None
        self.currentPlayer = None
        self.message = None

    # generate deck from carList.txt
    # cards are arrays ex. ['1', '1', 'one']
    def generateDeck(self):
        # initialize deck from carList.txt
        with open("cardList.txt") as f:
            self.deck = [Card(card.split(',')) for card in f.read().splitlines()]
        self.drawPile = list(self.deck)
        self.shuffleDeck()

    # shuffles the draw pile deck
    def shuffleDeck(self):
        random.shuffle(self.drawPile)

    # returns and removes last card in deck
    def drawCard(self):
        # if draw pile is empty, shuffle discard pile into it
        if len(self.drawPile) == 0:
            self.drawPile = list(self.discardPile)
            self.shuffleDeck()
            self.discardPile = []

        # remove last card from draw pile and return it
        topCard = self.drawPile[-1]
        self.drawPile.pop(-1)
        return topCard

    # deals the cards to the players
    async def dealCards(self):
        # deal each play 7 cards
        player: Player
        for player in self.players.values():
            for i in range(7):
                player.hand.append(self.drawCard())

            # sort hand and send to player
            player.hand.sort(key=lambda card: card.id)
            await player.sendHand("You were dealt the following cards:")

    async def showTable(self, ctx, showPlayers=True):
        if self.status == "setup":
            table = ''
            for playerID in self.players:
                player = self.players[playerID]
                table += f'{player.user} ({player.user.display_name})\n'
            message = Embed(title="The following people have joined the game:", description=table, color=0x00CFCF)
            message.set_footer(text="The game can start when at least 3 people have joined.")
            await ctx.send(embed=message)
        else:
            message = Embed(title=f'The current card in play is: {self.currentCard}', description=f'It is **{self.currentPlayer.user.display_name}\'s** turn!', color=0x00CFCF)
            if showPlayers:
                table = ''
                for playerID in self.players:
                    player = self.players[playerID]
                    table += f'{player.user.display_name} | {len(player.hand)} card{"s" if len(player.hand) > 1 else ""}.\n'
                message.add_field(name="Here are the players in this game:", value=table)
            await ctx.send(embed=message)

    def canPlay(self):
        return True

    def validPlay(self, message, player):
        return True

    def validMove(self, message):
        # message must be sent by current player and must either be a play, draw, or nope! command
        if message.author.id == self.currentPlayer.user.id and (message.content.lower()[:2] == "!p" or message.content.lower()[:2] == "!d" or message.content.lower()[:5] == "nope!"):
            # called nope
            if message.content.lower()[:5] == "nope!":
                if self.currentPlayer.drewCard == False:
                    self.message = "You cannot say nope! yet."
                    return False
                else:
                    self.currentPlayer.drewCard = False
                    if not self.canPlay():
                        self.message = f'Nope! {self.currentPlayer.user.display_name} cannot play a card!'
                        self.getNextPlayer()
                        return True
                    else:
                        self.message = "You are able to play because of the card you drew, try again."
                        return False
            # attempted to draw
            elif message.content.lower()[:2] == "!d":
                if not self.canPlay():
                    if self.currentPlayer.drewCard == True:
                        self.message = "You already drew a card!"
                        return False
                    else:
                        self.currentPlayer.drewCard = True
                        self.message = f'{self.currentPlayer.user.display_name} cannot play a card!\nDraw one card.  If you can play after drawing: play, if you still cannot: say **Nope!**'
                        return True
                else:
                    self.message = "You are able to play, try again."
                    return False
            # attempted to play
            else:
                if not self.canPlay():
                    self.message = "You cannot play any card.  Draw if you have not drawn yet, say nope! if you have already drawn."
                    return False
                else:
                    play = message.content.split()[1:]
                    if self.validPlay(play, self.currentPlayer):
                        self.message = "Valid play"
                        self.getNextPlayer()
                        return True
                    else:
                        self.message = "Invalid play."
                        return False
        return False

    def getNextPlayer(self):
        playerList = list(self.players.keys())
        self.currentPlayer = self.players[playerList[(playerList.index(self.currentPlayer.user.id) + 1) % len(playerList)]]


    # debugging info
    def __repr__(self):
        return f'players: {self.players}, numPlayers: {self.numPlayers}, status: {self.status}'