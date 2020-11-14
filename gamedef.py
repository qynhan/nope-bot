import discord
import random
from playerdef import Player

class Game:
    # constructor
    def __init__(self):
        self.players = {}
        self.numPlayers = 0
        self.status = "setup"
        self.deck = []

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

    # generate deck from carList.txt
    # cards are arrays ex. ['1', '1', 'one']
    def generateDeck(self):
        # initialize deck from carList.txt
        with open("cardList.txt") as f:
            self.deck = [card.split(',') for card in f.read().splitlines()]
        self.shuffleDeck()

    # shuffles the deck
    def shuffleDeck(self):
        random.shuffle(self.deck)

    # returns and removes last card in deck
    def drawCard(self):
        # todo when the deck runs out of cards
        if len(self.deck) != 0:
            topCard = self.deck[-1]
            self.deck.pop(-1)
            return topCard

    # debugging info
    def __repr__(self):
        return f'players: {self.players}, numPlayers: {self.numPlayers}, status: {self.status}'