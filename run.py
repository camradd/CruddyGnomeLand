import TileObject, World, Creature, pyglet

f = None
data = None

SIZE_X = 75
SIZE_Y = 45
tileSize = 16
world = World.World(SIZE_X, SIZE_Y)

def newWindow():
    return pyglet.window.Window(
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

window = newWindow()

@window.event
def on_draw():
    setSpriteImages()
    batch.draw()
    getCurrentState().draw()

def getCurrentState():
    return pyglet.text.Label('time step: %d  born: %d  dead: %d  alive: %d' %(world.time, world.born,
                              world.dead, world.alive),
                              font_name='mono',
                              font_size= 10,
                              x=window.width / 100, y=window.height / 100,
                              anchor_x='left', anchor_y='bottom')

def setSpriteImages():
    for row in range(SIZE_Y):
        for col in range(SIZE_X):
            tileObject = world.tiles[row][col].visibleTileObject()
            img = tileImages[tileObject.__class__]
            sprites[row][col].image = img

def step(dx):
    world.step()

    if world.saveData == 'tstep':
            data = "%d %d %d %d\n" %(world.time, world.born, world.dead, world.alive)
            f.write(data)

pyglet.clock.schedule_interval(step, 0.01)


def main():
    print "To create world type 'new world'"
    print "To begin simulation type 'run'."
    print "To exit simulation, exit window."
    print "To quit program type 'quit'."
    print "To save data from run, type 'create file'."

    while True:
        commandLine = raw_input(">>> ")
        if commandLine == 'new world':
            global world
            world = World.World(SIZE_X, SIZE_Y)

        if commandLine == 'new window':
            global window
            window = newWindow()

        if commandLine == 'run':
            pyglet.app.run()

        if commandLine == 'create file':
            timestepData = raw_input("'yes' or 'no', save timestep data?\n >>> ")
            filename = raw_input("enter file name: ")
            global f
            f = open(filename, 'w')

            if timestepData == 'yes':
                f.write('timestep born dead alive\n')
                world.saveData = 'tstep'
            else:
                world.saveData = 'onlyGenes'

        if commandLine == 'quit':
            if world.saveData != False:
                genomes = [c.genome for c in world.getCreatures()]
                s = str(genomes)
                f.write(s)
                f.close()
            return False

        else: pass




main()
