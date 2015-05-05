from World import *
import pyglet

SIZE_X = 120
SIZE_Y = 70
tileSize = 10

world = World(SIZE_X, SIZE_Y)

window = pyglet.window.Window(
    width  = SIZE_X * tileSize,
    height = SIZE_Y * tileSize
)

@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    sprites = createSprites(batch)
    window.clear()
    batch.draw()

def createSprites(batch):
    sprites = []

    for row in range(SIZE_Y):
        for col in range(SIZE_X):

            tile = world.tiles[row][col]
            img = None

            if tile.__class__ is Tree:
                img = pyglet.resource.image('data/tree.png')
            elif tile.__class__ is Food:
                img = pyglet.resource.image('data/food.png')
            else:
                img = pyglet.resource.image('data/tile.png')

            img.width = tileSize
            img.height = tileSize

            sprites.append(
                pyglet.sprite.Sprite(
                    img, col * tileSize, row * tileSize, batch=batch)
            )

    return sprites

pyglet.app.run()
