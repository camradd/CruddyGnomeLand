import random, Tile, TileObject, Creature

class World:

    tileObjectClasses = \
        [None, TileObject.Food, TileObject.Tree, Creature.Creature]
    tileObjectProbs = \
        [97  , 0.8            , 1.7            , 0.5              ]

    def __init__(self, width = 100, height = 100):
        self.tiles = \
            [[self.createTile(x, y) for x in range(width)] for y in range(height)]

        self.width = width
        self.height = height

    def createTile(self, x, y):
        tile = Tile.Tile(x, y)
        tileObjectClass = \
            self._weightedChoice(self.tileObjectClasses, self.tileObjectProbs)
        if tileObjectClass != None:
            tile.addTileObject(tileObjectClass())
        return tile

    def _weightedChoice(self, elements, weights):
        randomNumber = random.uniform(0, sum(weights))
        w = 0
        for i in range(len(weights)):
            w += weights[i]
            if w > randomNumber:
                return elements[i]
        return random.choice(elements)

    def getNearbyCreatures(self, creature, distance=4):
        creatures = []
        for yd in range(-distance, distance+1):
            for xd in range(-distance, distance+1):
                if yd == 0 and xd == 0: continue
                y, x = y + yd % self.height, x + xd % self.width
                c = self.tiles[y][x].tileObjectForType(Creature.Creature)
                if c != None: creatures.append[c]
        return creatures

    def getSight(self, creature, distance=4):
        '''
         [W, E, N, S] where each is three floats from 0 to 1 (food, tree, creature).
         It's a flat array. The float specifies closeness (0 is farther).
        '''
        sight = [0] * (len(tileObjectClasses) - 1)
        i = 0
        loc = (creature.tile.x, creature.tile.y)
        for axis in [0, 1]:
            for d in [-1, 1]:
                for toClass in tileObjectClasses:
                    if toClass == None: continue
                    for dist in range(distance):
                        nLoc = copy.deepcopy(loc)
                        nLoc[axis] = (nLoc[axis] + (d * (dist + 1)))\
                            % (self.width if axis == 0 else self.height)
                        x, y = nLoc
                        if self.tiles[y][x].containsType(toClass):
                            sight[i] = 1 - (dist / (distance + 1))
            i += 1
        return sight

    def act(self, creature, action):
        axis = action[0]
        d = -1 if action[1] == 0 else 1
        loc = (creature.tile.x, creature.tile.y)
        loc[axis] = (loc[axis] + d) % (self.width if axis == 0 else self.height)
        x, y = loc
        tile = self.tiles[y][x]
        creature.changeHealth(tile.effect(creature))
        if (tile.canEnter(creature)):
            creature.tile.removeTileObject(creature)
            tile.addTileObject(creature)

    def removeCreature(self, creature):
        creature.tile.removeTileObject(creature)
