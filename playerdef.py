import discord

# the colors the letters represent
letterColors = {'r' : 'red', 'y' : 'yellow', 'b' : 'blue', 'g' : 'green', 'w' : 'wild',
                'n': 'nominate', 'i' :'invisible', 'R' : 'reset'}

class Player:
    # constructor, takes user argument - a discord object representing a user
    def __init__(self, user : discord.user):
        self.user = user
        self.hand = []
        self.play = []

    def haveCard(self, cardString):
        haveCard = False

        for card in self.hand:
            if haveCard:
                return haveCard
            for i in len(cardString):
                if letterColors(cardString[i]) in card.colors or letterColors(cardString[i]) == card.value :
                    haveCard = True
                else:
                    haveCard = False

        return haveCard

    def getCard(self, cardString):
        theCard = False

        for card in self.hand:
            if theCard:
                return self.hand.pop(self.hand.index(card))
            for i in len(cardString):
                if letterColors(cardString[i]) in card.colors or letterColors(cardString[i]) == card.value:
                    theCard = True
                else:
                    theCard = False

        return theCard

    # string representation for print statements
    def __str__(self):
        return f'{self.user}'

    # debugging info
    def __repr__(self):
        return f'user: {self.user}'