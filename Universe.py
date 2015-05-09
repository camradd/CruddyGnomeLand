import World, TileObject, Creature, pyglet
import mongoengine as db

class Universe(db.Document):

    def _makeTileImg(self, path):
        img = pyglet.resource.image(path)
        img.width = self.tileSize
        img.height = self.tileSize
        return img

    def __init__(self, name, width = 75, height = 45, tileSize = 16, stepTime = 0.1):
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
            height = height * tileSize,
            visible = False,
            caption = self.name
        )
        self.batch = pyglet.graphics.Batch()
        self.sprites = [
            [pyglet.sprite.Sprite(self._tileObjectImages[TileObject.TileObject],
                    col * self.tileSize, row * self.tileSize, batch=self.batch)
                for col in range(self.width)]
            for row in range(self.height)
        ]

        self.window.set_handler('on_draw', lambda: self.on_draw())
        self.setStepTime(stepTime)

    def setStepTime(self, time):
        pyglet.clock.unschedule(self.step)
        pyglet.clock.unschedule(self.stepFast)

        if time == 0:
            pyglet.clock.schedule_interval(self.stepFast, 0.001)
        else:
            pyglet.clock.schedule_interval(self.step, time)

    def step(self, dt = 0):
        self.world.step()

    def stepFast(self, dt = 0):
        self.world.step(5)

    def show(self, activate = True):
        self.window.set_visible(True)
        if activate: self.window.activate()
    def hide(self):
        self.window.set_visible(False)
    def toggle(self):
        self.window.set_visible(not self.window.visible)

    def on_draw(self):
        if not self.window.visible: return
        self._updateSpriteImages()
        self.window.clear()
        self.batch.draw()
        self.stateLabel.draw()

    @property
    def stateLabel(self):
        return pyglet.text.Label('time step: %d  born: %d  dead: %d  alive: %d' % (
            self.world.time, self.world.born, self.world.dead, self.world.alive),
            font_name='mono', font_size= 10,
            x=self.window.width / 100, y=self.window.height / 100,
            anchor_x='left', anchor_y='bottom')

    def _updateSpriteImages(self):
        for row in range(self.height):
            for col in range(self.width):
                tileObject = self.world.tiles[row][col].visibleTileObject()
                img = self._tileObjectImages[tileObject.__class__]
                self.sprites[row][col].image = img
