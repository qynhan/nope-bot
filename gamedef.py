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

    def checkTwo(self, card1, card2):
        for color in card1.colors:
            if color in card2.colors:
                return True
        return False


    # precondition the number on the top card is the same as the number of cards played
    def validPlay(self, message, player):
        topCard = self.currentCard
        cardList = []
        pickedCards = message.split(" ")
        for card in pickedCards:
            if not player.haveCard(card):
                return False
        for i in range(len(pickedCards)):
            cardList.append(player.getCard(pickedCards[i]))














        # if topCard.value == "one":
        #     return self.checkTwo(cardList[0], topCard)
        # if topCard.values == "two":
        #     if not self.checkTwo(cardList[0], cardList[1]) \
        #             or not self.checkTwo(cardList[0], topCard) \
        #             or not self.checkTwo(cardList[1], topCard):
        #         return False
        # if topCard.value == "three":
        #     if not self.checkTwo(cardList[0], cardList[1]) \
        #             or not self.checkTwo(cardList[0], cardList[2]) \
        #             or not self.checkTwo(cardList[1], cardList[2]) \
        #             or not self.checkTwo(cardList[0], topCard) \
        #             or not self.checkTwo(cardList[1], topCard) or \
        #             not self.checkTwo(cardList[2], topCard) :
        #         return False
        # return True

    # debugging info
    def __repr__(self):
        return f'players: {self.players}, numPlayers: {self.numPlayers}, status: {self.status}'