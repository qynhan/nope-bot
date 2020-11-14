import discord

class Player:
    # constructor, takes user argument - a discord object representing a user
    def __init__(self, user : discord.user):
        self.user = user
        self.hand = []

    # string representation for print statements
    def __str__(self):
        return f'{self.user}'

    # debugging info
    def __repr__(self):
        return f'user: {self.user}, hand: {self.hand}'