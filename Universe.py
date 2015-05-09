import World, TileObject, Creature, pyglet

class Universe:

    def _makeTileImg(self, path):
        img = pyglet.resource.image(path)
        img.width = self.tileSize
        img.height = self.tileSize
        return img

    def __init__(self, name, width = 75, height = 45, tileSize = 16):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.name = name

        self._tileObjectImages = {
            TileObject.Tree:       self._makeTileImg('img/tree.png'),
            TileObject.Food:       self._makeTileImg('img/food.png'),
            TileObject.TileObject: self._makeTileImg('img/tile.png'),
            Creature.Creature:     self._makeTileImg('img/creature.png')
        }

        self.world = World.World(width, height)
        self.window = pyglet.window.Window(
            width  = width * tileSize,
            height = height * tileSize
        )
        self.window.set_caption(self.name)
        self.batch = pyglet.graphics.Batch()
        self.sprites = [
            [pyglet.sprite.Sprite(self._tileObjectImages[TileObject.TileObject],
                    col * self.tileSize, row * self.tileSize, batch=self.batch)
                for col in range(self.width)]
            for row in range(self.height)
        ]

        self.window.set_handler('on_draw', lambda: self.on_draw())
        pyglet.clock.schedule_interval(lambda dx: self.step(), 0.01)

    def step(self):
        self.world.step()

    def on_draw(self):
        self._updateSpriteImages()
        self.window.clear()
        self.batch.draw()
        self.stateLabel.draw()

    @property
    def stateLabel(self):
        return pyglet.text.Label('time step: %d  born: %d  dead: %d  alive: %d  avg age: %.2f' % (
            self.world.time, self.world.born, self.world.dead,
            self.world.alive, self.world.avgAge()),
            font_name='mono', font_size= 10,
            x=self.window.width / 100, y=self.window.height / 100,
            anchor_x='left', anchor_y='bottom')

    def _updateSpriteImages(self):
        for row in range(self.height):
            for col in range(self.width):
                tileObject = self.world.tiles[row][col].visibleTileObject()
                img = self._tileObjectImages[tileObject.__class__]
                self.sprites[row][col].image = img
