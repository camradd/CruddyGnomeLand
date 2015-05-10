import random, TileObject, Creature

class Tile(object):

    '''
     The Tile class represents a single tile in the world. It has TileObjects as
     children that represent things inside the tile (tree, food, creature, etc).
     The TileObjects decide their effects and accessability, which is prograted
     up to the Tile and summed/or logically conjoined.
    '''

    def __init__(self, x, y, world):
        to = TileObject.TileObject()
        to.tile = self
        self.tileObjects = [to]
        self.x = x
        self.y = y
        self.world = world

    '''
     Adds a tile object in this tile. Rules about with objects can coexist are
     currently enforced crudely using the visibilityIndex.
    '''
    def addTileObject(self, tileObject):
        if self.visibleTileObject().visibilityIndex > tileObject.visibilityIndex:
            return
        tileObject.tile = self
        self.tileObjects.append(tileObject)

    def removeTileObject(self, tileObject):
        tileObject.tile = None
        self.tileObjects.remove(tileObject)

    def visibleTileObject(self):
        r = self.tileObjects[0]
        for tileObject in self.tileObjects:
            if tileObject.visibilityIndex > r.visibilityIndex:
                r = tileObject
        return r

    def isEmpty(self):
        return len(self.tileObjects) == 1

    def tileObjectForType(self, tileObjectType):
        for tileObject in self.tileObjects:
            if tileObject.__class__ is tileObjectType:
                return tileObject
        return None

    def containsType(self, tileObjectType):
        return self.tileObjectForType(tileObjectType) != None

    def effect(self, creature):
        return sum([to.effect(creature) for to in self.tileObjects])

    def canEnter(self, creature):
        return not (False in [to.canEnter(creature) for to in self.tileObjects])

    def step(self):
        if random.uniform(0, 1) < 0.00001:
            self.addTileObject(TileObject.Food())

        for tileObject in self.tileObjects:
            # Tile objects can move during their step, and then get stepped again in their
            # new tile. So we use a boolean flag to keep that from happening.
            if tileObject._stepping: continue
            tileObject._stepping = True
            tileObject.step()

    def stepFinished(self):
        for tileObject in self.tileObjects:
            if not tileObject._stepping: continue
            tileObject._stepping = False
            tileObject.stepFinished()
