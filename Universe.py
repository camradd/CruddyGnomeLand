import World, TileObject, Creature, pyglet, datetime, merge

try:
    import mongoengine as db
except ImportError:
    import db_fill as db

db.connect('cruddy_gnome_land')

class Universe(db.Document):

    def _makeTileImg(self, path):
        img = pyglet.resource.image(path)
        img.width = self.tileSize
        img.height = self.tileSize
        return img

    name = db.StringField()
    world = db.ReferenceField('World', reverse_delete_rule=db.DENY)
    created = db.DateTimeField(default=datetime.datetime.now)
    modified = db.DateTimeField()
    runData = db.ListField(db.DictField())
    settings = db.DictField()

    def __init__(self, name, settings = {}, tileSize = 16, stepTime = 0.1):
        db.Document.__init__(self)

        defaultSettings = {
            'world': {
                'width': 75,
                'height': 45,
                'creature': {}
            },
            'saveFreq' : 10
        }
        if not self.settings:
            self.settings = merge.mergeDict(defaultSettings, settings)
        else:
            self.settings = merge.mergeDict(defaultSettings, self.settings)

        width = self.width = self.settings['world']['width']
        height = self.height = self.settings['world']['height']
        self.tileSize = tileSize
        self.name = name

        self._tileObjectImages = {
            TileObject.Tree:       self._makeTileImg('img/tree.png'),
            TileObject.Food:       self._makeTileImg('img/food.png'),
            TileObject.TileObject: self._makeTileImg('img/tile.png'),
            Creature.Creature:     self._makeTileImg('img/creature.png')
        }

        self.world = World.World(self.settings['world'])
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

    def clean(self):
        self.modified = datetime.datetime.now
        self.runData.append({
            'time': self.world.time,
            'born': self.world.born,
            'dead': self.world.dead,
            'alive': self.world.born - self.world.dead,
            'avgAge': self.world.avgAge
        })
        self.world.save()
        for c in self.world.population:
            c.save()

    def setStepTime(self, time):
        pyglet.clock.unschedule(self.step)
        pyglet.clock.unschedule(self.stepFast)

        if time == 0:
            pyglet.clock.schedule_interval(self.stepFast, 0.001)
        else:
            pyglet.clock.schedule_interval(self.step, time)

    def step(self, dt = 0):
        self.world.step()
        if self.world.time % self.settings["saveFreq"] == 1: self.save()

    def stepFast(self, dt = 0):
        self.world.step(10)
        self.save()

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
        return pyglet.text.Label(
            'time step: %d  born: %d  dead: %d  alive: %d  avg age: %.2f' % (
            self.world.time, self.world.born, self.world.dead,
            self.world.alive, self.world.avgAge),
            font_name='mono', font_size= 10,
            x=self.window.width / 100, y=self.window.height / 100,
            anchor_x='left', anchor_y='bottom')

    def _updateSpriteImages(self):
        for row in range(self.height):
            for col in range(self.width):
                tileObject = self.world.tiles[row][col].visibleTileObject()
                img = self._tileObjectImages[tileObject.__class__]
                self.sprites[row][col].image = img
