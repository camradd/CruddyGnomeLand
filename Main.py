import World, pyglet

SIZE_X = 120
SIZE_Y = 70
tileSize = 10
world = World.World(SIZE_X, SIZE_Y)

window = pyglet.window.Window(
    width  = SIZE_X * tileSize,
    height = SIZE_Y * tileSize
)

def makeImg(path):
    img = pyglet.resource.image(path)
    img.width = tileSize
    img.height = tileSize
    return img

batch = pyglet.graphics.Batch()
tileImages = {
    World.Tree: makeImg('data/tree.png'),
    World.Food: makeImg('data/food.png'),
    World.Tile: makeImg('data/tile.png')
}
sprites = [
    [pyglet.sprite.Sprite(tileImages[World.Tile], col*tileSize, row*tileSize, batch=batch)
        for col in range(SIZE_X)]
    for row in range(SIZE_Y)
]

@window.event
def on_draw():
    setSpriteImages()
    # window.clear()
    batch.draw()

def setSpriteImages():
    for row in range(SIZE_Y):
        for col in range(SIZE_X):
            tile = world.tiles[row][col]
            img = tileImages[tile.__class__]
            sprites[row][col].image = img

def update(dt):
    global world
    world = World.World(SIZE_X, SIZE_Y)
pyglet.clock.schedule_interval(update, 0.3)

pyglet.app.run()
