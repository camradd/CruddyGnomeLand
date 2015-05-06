import random, Creature

class Tile:

    '''
     The Tile class represents a single tile in the world. It has TileObjects as
     children that represent things inside the tile (tree, food, creature, etc).
     The TileObjects decide their effects and accessability, which is prograted
     up to the Tile and summed/or logically conjoined.
    '''

    def __init__(self):
        self.tileObjects = [TileObject()]

    '''
     Adds a tile object in this tile. Rules about with objects can coexist are
     currently enforced crudely using the visibilityIndex.
    '''
    def addTileObject(self, tileObject):
        if self.visibleTileObject().visibilityIndex>tileObject.visibilityIndex:
            return
        self.tileObjects.push(tileObject)

    def removeTileObject(self, tileObject):
        self.tileObjects.remove(tileObject)

    def visibleTileObject(self):
        r = tileObjects[0]
        for tileObject in self.tileObjects:
            if tileObject.visibilityIndex > r.visibilityIndex:
                r = tileObject
        return r

    def tileObjectForType(self, tileObjectType):
        for tileObject in self.tileObjects:
            if tileObject.__class__ is tileObjectType:
                return tileObject
        return None

    def containsType(self, tileObjectType):
        return self.tileObjectType != None

    def effect(self, creature):
        return sum([to.effect(creature) for to in self.tileObjects])

    def canEnter(self, creature):
        return not (False in [to.canEnter(creature) for to in self.tileObjects])

    def step(self):
        if random.uniform(0, 1) < 0.005:
            self.addTileObject(Food())

        for tileObject in self.tileObjects:
            tileObject.step()

    def stepFinished(self):
        for tileObject in self.tileObjects:
            tileObject.stepFinished()

class TileObject:

    '''
     The TileObject class represents something inside a tile in the world
     (tree, food, creature, etc). The TileObjects decide their effects and
     accessability, which is prograted up to the Tile and summed/or logically
     conjoined. The base class TileObject represents the ground.
    '''
    visibilityIndex = 0

    def effect(self, creature):
        return 0

    def canEnter(self, creature):
        return True

    def step(self):
        pass

    def stepFinished(self):
        pass

class Food(TileObject):

    '''
    Food object. Has variable nutrition value, which represents the amount of
    health increase it causes.
    '''
    visibilityIndex = 5

    def effect(self, creature):
        return 0.2

class Tree(TileObject):

    '''
    Tree object, in world. Carries a damage value.
    '''

    visibilityIndex = 15

    def effect(self, creature):
        return -0.2

class World:

    tileObjectClasses   = [None, Food, Tree, Creature.Creature]
    tileObjectProbs     = [97  , 0.8 , 1.7 , 0.05             ]

    def __init__(self, width = 100, height = 100):
        self.tiles = \
            [[self.createTile() for x in range(width)] for y in range(height)]

        for i in range(width * height * 0.05):
            self.spawnCreature(Creature.Creature())

        self.width = width
        self.height = height

    def createTile(self):
        tile = Tile()
        tileObjectClass = \
            self._weightedChoice(self.tileObjectClasses, self.tileObjectProbs)
        if tileObjectClass != None:
            tile.addTileObject(tileObjectClass())

    def _weightedChoice(self, elements, weights):
        randomNumber = random.uniform(0, sum(weights))
        w = 0
        for i in range(len(weights)):
            w += weights[i]
            if w > randomNumber:
                return elements[i]
        # all weights are 0
        return random.choice(elements)


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
