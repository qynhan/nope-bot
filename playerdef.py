import discord
from discord import Embed

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

    # send the player their hand, title is a string that will be the beginning of the message to the player
    async def sendHand(self, title):
        # make a list of their cards
        handDisplay = ''
        for card in self.hand:
            handDisplay += str(card) + ' | '

        # remove the extra | from the end
        handDisplay = handDisplay[:-3]

        # dm user
        message = Embed(title=title, description=handDisplay, color=0x00CFCF)
        message.set_footer(text=f'You currently have {len(self.hand)} card{"s" if len(self.hand) > 1 else ""}.')
        await self.user.send(embed=message)


    # string representation for print statements
    def __str__(self):
        return f'{self.user}'

    # debugging info
    def __repr__(self):
        return f'user: {self.user}, hand: {self.hand}'