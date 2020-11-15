import discord
from discord import Embed
import random
from playerdef import Player
from carddef import Card

letterColors = {'r': '1', 'y': '2', 'b': '3', 'g': '4', 'w': '5'}
letterType = {'1': 'one', '2': 'two', '3': 'three'}


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
    def addPlayer(self, user: discord.User):
        # do not add someone who already joined
        playerAdded = False
        if user.id not in self.players:
            self.players[user.id] = (Player(user))
            self.numPlayers += 1
            playerAdded = True

        return playerAdded

    # remove player from game, takes in user who ran the quit command
    def removePlayer(self, user: discord.User):
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
            message = Embed(title=f'The current card in play is: {self.currentCard}',
                            description=f'It is **{self.currentPlayer.user.display_name}\'s** turn!', color=0x00CFCF)
            if showPlayers:
                table = ''
                for playerID in self.players:
                    player = self.players[playerID]
                    table += f'{player.user.display_name} | {len(player.hand)} card{"s" if len(player.hand) > 1 else ""}.\n'
                message.add_field(name="Here are the players in this game:", value=table)
            await ctx.send(embed=message)


    def strToCardList(self, message):
        # ex. br3 bg2
        cardList = []

        for word in message.split(' '):
            card_arr = []
            if len(word) > 3:
                return None
            if word[0] not in list(letterColors) \
                    or word[1] not in list(letterColors) \
                    or word[2] not in list(letterType):
                return None
            card_arr.append(letterColors[word[0]])
            card_arr.append(letterColors[word[1]])
            card_arr.append(letterType[word[2]])
            cardList.append(Card(card_arr))
        return cardList

    # precondition the number on the top card is the same as the number of cards played
    def validPlay(self, message, player):
        # check cards in hand
        # check colors
        # get rid of cards from hand

        # new plan
        # string input
        # if its valid cards
        # cardList =  array of card objects
        # compare cards in checklist to hand
        # check cardlist with currentCard

        # create list of card object from string message
        cardList = self.strToCardList(message)
        if not cardList:
            return False

        for card in cardList:
            if card not in player.hand:
                return False

        for check_color in self.currentCard.colors:  # current card is blue red
            isValidColor = True
            for card in cardList:
                if check_color not in card.colors:
                    isValidColor = False
                    break
            if isValidColor:
                return True
        return False


    # debugging info
    def __repr__(self):
        return f'players: {self.players}, numPlayers: {self.numPlayers}, status: {self.status}'
