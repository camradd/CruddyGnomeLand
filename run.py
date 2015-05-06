import TileObject, World, Creature, pyglet

SIZE_X = 75
SIZE_Y = 45
tileSize = 16
world = World.World(SIZE_X, SIZE_Y)

window = pyglet.window.Window(
    width  = SIZE_X * tileSize,
    height = SIZE_Y * tileSize
)

def makeTileImg(path):
    img = pyglet.resource.image(path)
    img.width = tileSize
    img.height = tileSize
    return img

batch = pyglet.graphics.Batch()
tileImages = {
    TileObject.Tree:       makeTileImg('img/tree.png'),
    TileObject.Food:       makeTileImg('img/food.png'),
    TileObject.TileObject: makeTileImg('img/tile.png'),
    Creature.Creature:     makeTileImg('img/creature.png')
}
sprites = [
    [pyglet.sprite.Sprite(tileImages[TileObject.TileObject],
                            col*tileSize, row*tileSize, batch=batch)
        for col in range(SIZE_X)]
    for row in range(SIZE_Y)
]



@window.event
def on_draw():
    currentTime = pyglet.text.Label('%d' %world.time,
                              font_name='mono',
                              font_size= 12,
                              x=window.width//100, y=window.height//100,
                              anchor_x='left', anchor_y='bottom')
    setSpriteImages()
    batch.draw()
    currentTime.draw()

def setSpriteImages():
    for row in range(SIZE_Y):
        for col in range(SIZE_X):
            tileObject = world.tiles[row][col].visibleTileObject()
            img = tileImages[tileObject.__class__]
            sprites[row][col].image = img

def step(dx):
    world.step()

pyglet.clock.schedule_interval(step, 0.01)

pyglet.app.run()
