import World, pyglet

SIZE_X = 120
SIZE_Y = 70
tileSize = 10
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
    World.Tree: makeTileImg('img/tree.png'),
    World.Food: makeTileImg('img/food.png'),
    World.Tile: makeTileImg('img/tile.png')
}
sprites = [
    [pyglet.sprite.Sprite(tileImages[World.Tile], col*tileSize, row*tileSize,
                            batch=batch)
        for col in range(SIZE_X)]
    for row in range(SIZE_Y)
]

@window.event
def on_draw():
    setSpriteImages()
    batch.draw()

def setSpriteImages():
    for row in range(SIZE_Y):
        for col in range(SIZE_X):
            tile = world.tiles[row][col]
            img = tileImages[tile.__class__]
            sprites[row][col].image = img

pyglet.app.run()
