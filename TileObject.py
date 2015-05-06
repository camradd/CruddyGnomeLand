class TileObject:

    '''
     The TileObject class represents something inside a tile in the world
     (tree, food, creature, etc). The TileObjects decide their effects and
     accessability, which is prograted up to the Tile and summed/or logically
     conjoined. The base class TileObject represents the ground.
    '''
    visibilityIndex = 0
    tile = None

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

    def canEnter(self, creature):
        self.tile.removeTileObject(self)
        return True

class Tree(TileObject):

    '''
    Tree object, in world. Carries a damage value.
    '''

    visibilityIndex = 15

    def effect(self, creature):
        return -0.2

    def canEnter(self, creature):
        return False
