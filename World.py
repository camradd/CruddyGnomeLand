import random
from Creature import *

class Tile:

    def __init__(self):
        self.contains = None

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

    tileClasses = [Tile, Food, Tree, Creature]
    tileProbs   = [97  , 1   , 2   ,    0    ]

    def __init__(self, width = 100, height = 100):
        self.tiles = \
            [[self.createTile() for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

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

    def generatePopulation(size = 20):
        population = [Creature() for i in range(size)]
        xTiles = range(self.width)
        yTiles = range(self.height)
        while population != []:
            tileX = random.choice(xTiles)
            tileY = random.choice(yTiles)
            self.tiles[tileX][tileY].contains = random.choice(population)
            xTiles.remove(tileX)
            yTiles.remove(tileY)


    '''
     Are actions handled in World class? We can move this to the Creature, but it
     made most sense to me here, based on what we have now. Here is a reproduction
     method that can handle any number of parents.
    '''

    def reproduction(parents):
        parents = [p.genome for p in parents]
        if len(parents) == 1:
            return Creature(mutation(parents[0]))
        else:
            while len(parents) > 1:
                p1 = random.choice(parents)
                parents.remove(p1)
                p2 = random.choice(parents)
                parents.remove(p2)
                parents.append(crossover(p1,p2))
            return Creature(mutation(parents[0]))

    def mutation(genome, rate = .3):
        return [
            g + random.uniform(-.5,.5) if \
            random.uniform(0,1) < rate else g for g in genome
        ]

    def crossover(mateGenome, partnerGenome):
        pivot = random.choice(range(len(mateGenome)))
        return [
            mateGenome[i] if i < pivot else \
            partnerGenome[i] for i in range(len(mateGenome))
        ]
