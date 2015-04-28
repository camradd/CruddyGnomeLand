from World import *
import math, time

SIZE_X = 120
SIZE_Y = 70
tileSize = 10
width = SIZE_X * tileSize
height = SIZE_Y * tileSize

world = World(SIZE_X, SIZE_Y)

def setup():
    size(width, height)
    noStroke()

def draw():

    for row in range(SIZE_Y):
        for col in range(SIZE_X):

            tile = world.tiles[row][col]
            img = None

            if tile.__class__ is Tree:
                img = loadImage('tree.png')
            elif tile.__class__ is Food:
                img = loadImage('food.png')
            else:
                img = loadImage('tile.png')

            image(img, col * tileSize, row * tileSize, tileSize, tileSize)
