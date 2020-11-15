import discord
from discord import Embed
import random
import copy
from playerdef import Player
from carddef import Card

letterColors = {'r': '1', 'y': '2', 'b': '3', 'g': '4', 'w': '5'}
letterType = {'1': 'one', '2': 'two', '3': 'three'}
# what 3rd sorting digit corresponds to what value
valueNums = {'one' : 1, 'two' : 2, 'three' : 3, 'nominate' : 4, 'invisible' : 5, 'wild' : 6, 'reset' : 7}



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
        with open("plainCardList.txt") as f: # todo: change back to "cardList.txt" for all cards, change to "wildCardList.txt" to include wild cards and no action cards
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

    # temporary implementation for testing
    # send 0 to the prompt if to act as if the user cannot play a card, send anything else to indicate that they can play
    def canPlay(self):
        result = input("can play? ")
        if result == "0":
            return False
        else:
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
                        self.message = f'**Nope!** {self.currentPlayer.user.display_name} cannot play a card!'
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

                        # draw card and sort hand
                        self.currentPlayer.hand.append(self.drawCard())
                        self.currentPlayer.hand.sort(key=lambda card: card.id)
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
                    play = " ".join(message.content.split()[1:])
                    if self.validPlay(play, self.currentPlayer):
                        self.message = "Valid play"
                        self.getNextPlayer()
                        return True
                    else:
                        self.message = "Invalid play."
                        return False

    def strToCardList(self, message):
        # ex. br3 bg2
        cardList = []

        for word in message.split(' '):
            card_arr = []
            if len(word) != 3:
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

        if len(cardList) != valueNums[self.currentCard.value]:
            return False

        hand_copy = copy.deepcopy(player.hand)
        for card in cardList:
            if card not in hand_copy:
                return False
            else:
                hand_copy.remove(card)

        for check_color in self.currentCard.colors:  # ex. current card is blue red
            isValidColor = True
            for card in cardList:
                if check_color not in card.colors:
                    isValidColor = False
                    break
            if isValidColor:
                # put former current card in discard pile
                self.discardPile.append(self.currentCard)

                # remove card(s) from hand
                for i in range(len(cardList)):
                    card = player.hand.pop(player.hand.index(cardList[i]))
                    # make last card played the current card
                    if i == len(cardList) - 1:
                        self.currentCard = card
                    # put any other cards played in the discard pile
                    else:
                        self.discardPile.append(card)

                # todo: player leaves game when they run out of cards
                return True
        return False

    # sets current player to the next person
    def getNextPlayer(self):
        playerList = list(self.players.keys())
        self.currentPlayer = self.players[playerList[(playerList.index(self.currentPlayer.user.id) + 1) % len(playerList)]]


    # debugging info
    def __repr__(self):
        return f'players: {self.players}, numPlayers: {self.numPlayers}, status: {self.status}'
