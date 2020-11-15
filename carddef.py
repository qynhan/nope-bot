
# what colors the numbers from the text file represent
colorNums = {'1' : 'red', '2' : 'yellow', '3' : 'blue', '4' : 'green', '5' : 'wild'}

# what 3rd sorting digit corresponds to what value
valueNums = {'one' : 1, 'two' : 2, 'three' : 3, 'nominate' : 4, 'invisible' : 5, 'wild' : 6, 'reset' : 7}

# the emotes (or text) used to represent cards
emotes = {'red': '❤️', 'yellow' : '💛', 'blue' : '💙', 'green' : '💚', 'one' : '**1**', 'two' : '**2**',
          'three' : '**3**', 'nominate' : '👉', 'invisible' : '👁️', 'wild' : '**Wild**', 'reset' : '**Reset**'}

class Card:
    # constructor, takes in list of 3 strings: the first two are the card's colors and the third is its value
    def __init__(self, data):
        color1 = data[0]
        color2 = data[1]
        value = data[2]

        self.value = value
        self.id = valueNums[value]

        # wild color
        if color1 == '5':
            self.colors = [colorNums['1'], colorNums['2'], colorNums['3'], colorNums['4']]
            self.id += 500
        else:
            self.id += int(color1 + color2 + '0')

            # single-color
            if color1 == color2:
                self.colors = [colorNums[color1]]

            #double-color
            else:
                self.colors = [colorNums[color1], colorNums[color2]]

        # generate string representation
        self.rep = ''

        # double-color
        if len(self.colors) == 2:
            self.rep += emotes[self.colors[0]] + emotes[self.colors[1]]
        # single-color
        elif len(self.colors) == 1:
            self.rep += emotes[self.colors[0]]
        # wild card color is not shown

        self.rep += ' ' + emotes[self.value]

    # string representation for print statements
    def __str__(self):
        return self.rep

    # debugging info
    def __repr__(self):
        return f'value: {self.value}, colors: {self.colors}, id: {self.id}, str: {str(self)}'

    # check card equality
    def __eq__(self, other):
        return self.id == other.id