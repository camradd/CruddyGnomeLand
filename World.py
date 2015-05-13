import random, Tile, TileObject, Creature, copy, merge

try:
    import mongoengine as db
except ImportError:
    import db_fill as db

class World(db.Document):

    tileObjectClasses = [None, TileObject.Food, TileObject.Tree, Creature.Creature]
    tileObjectProbs   = [97  , 0.8            , 1.7            , 0.5              ]

    inhabitants = db.ListField(db.ReferenceField('Creature', reverse_delete_rule=db.PULL))

    born = 0
    time = 0
    dead = 0
    population = []

    def __init__(self, settings = {}):
        db.Document.__init__(self)

        defaultSettings = {
            'width': 100,
            'height': 100,
            'tileObjectProbs': self.tileObjectProbs,
            'creature': {}
        }
        self.settings = merge.mergeDict(defaultSettings, settings)

        self.tileObjectProbs = self.settings['tileObjectProbs']

        width = self.width = self.settings['width']
        height = self.height = self.settings['height']

        self.tiles = [[self.createTile(x, y) for x in range(width)] for y in range(height)]

    @property
    def alive(self):
        return self.born - self.dead

    def step(self, steps = 1):
        for step in range(steps):
            flatTiles = [self.tiles[r][c] for c in range(self.width) for r in range(self.height)]
            random.shuffle(flatTiles)

            for tile in flatTiles:
                tile.step()

            for tile in flatTiles:
                tile.stepFinished()

        self.time += steps

    def createTile(self, x, y):
        tile = Tile.Tile(x, y, self)
        tileObjectClass = \
            self._weightedChoice(self.tileObjectClasses, self.tileObjectProbs)
        if tileObjectClass != None:
            to = None
            if issubclass(tileObjectClass, Creature.Creature):
                to = tileObjectClass(None, self.settings['creature'])
                self._registerCreature(to)
            else:
                to = tileObjectClass()
            tile.addTileObject(to)
        return tile

    def _weightedChoice(self, elements, weights):
        randomNumber = random.uniform(0, sum(weights))
        w = 0
        for i in range(len(weights)):
            w += weights[i]
            if w > randomNumber:
                return elements[i]
        return random.choice(elements)

    @property
    def popSize(self):
        return len(self.population)

    @property
    def ages(self):
        return [c.age for c in self.population]

    @property
    def avgAge(self):
        return sum(self.ages) / float(self.popSize)

    def getNearbyCreatures(self, creature, distance=4):
        creatures = []
        x, y = creature.tile.x, creature.tile.y
        for yd in range(-distance, distance+1):
            for xd in range(-distance, distance+1):
                if yd == 0 and xd == 0: continue
                ny, nx = (y + yd) % self.height, (x + xd) % self.width
                c = self.tiles[ny][nx].tileObjectForType(Creature.Creature)
                if c != None: creatures.append(c)
        return creatures

    def getSight(self, creature, distance=4):
        '''
         [W, E, N, S] where each is three floats from 0 to 1 (food, tree, creature).
         It's a flat array. The float specifies closeness (0 is farther).
        '''
        sight = [0] * (distance * (len(self.tileObjectClasses) - 1))
        i = 0
        loc = [creature.tile.x, creature.tile.y]
        for axis in [0, 1]:
            for d in [-1, 1]:
                for toClass in self.tileObjectClasses:
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
        loc = [creature.tile.x, creature.tile.y]
        loc[axis] = (loc[axis] + d) % (self.width if axis == 0 else self.height)
        x, y = loc
        tile = self.tiles[y][x]
        creature.changeHealth(tile.effect(creature))
        if creature.health > 0 and tile.canEnter(creature):
            creature.tile.removeTileObject(creature)
            tile.addTileObject(creature)

    def _registerCreature(self, creature):
        self.born += 1
        self.inhabitants.append(creature)
        self.population.append(creature)

    def spawnCreature(self, creature):
        for t in range(200):
            x, y = random.choice(range(self.width)), random.choice(range(self.height))
            if self.tiles[y][x].isEmpty():
                self.tiles[y][x].addTileObject(creature)
                self._registerCreature(creature)
                return True
        print 'Overpopulation!'
        return False

    def removeCreature(self, creature):
        creature.tile.removeTileObject(creature)
        self.dead += 1
        self.population.remove(creature)

    def getCreatures(self):
        creatures = []
        for row in self.tiles:
            for tileY in row:
                c = tileY.tileObjectForType(Creature.Creature)
                if c != None: creatures.append(c)
        return creatures
