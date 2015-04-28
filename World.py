import random

class Tile:

    def __init__(self):
        pass

    def __repr__(self):
        return " "

class Food:

    '''
    Food object. Has variable nutrition value, which represents the amount of
    health increase it causes.
    '''

    def __init__(self):
        self.affect = 0.2

    def __repr__(self):
        return "f"

class Tree:

    '''
    Tree object, in world. Carries a damage value.
    '''

    def __init__(self):
        self.affect = -0.2

    def __repr__(self):
        return "T"

class World:

    tileClasses = [Tile, Food, Tree]
    tileProbs   = [97  , 1   , 2   ]

    def __init__(self, width = 100, height = 100):
        self.tiles = \
            [[self.createTile() for x in range(width)] for y in range(height)]

    def createTile(self):
        tileClass = self._weightedChoice(self.tileClasses, self.tileProbs)
        return tileClass()

    def _weightedChoice(self, elements, weights):
        randomNumber = random.uniform(0, sum(weights))
        w = 0
        for i in range(len(weights)):
            w += weights[i]
            if w > randomNumber:
                return elements[i]
        # all weights are 0
        return random.choice(elements)
