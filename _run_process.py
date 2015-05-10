import Universe, sys, pyglet, signal, time, json
from AsyncFIFORead import AsyncFIFORead

f = AsyncFIFORead(sys.stdin)

def readInput(dx):
    line = f.readline()
    if line == None: return
    try:
        print eval(line, globals(), globals())
    except:
        try:
            exec line in globals(), globals()
        except Exception as e:
            print e
    print '___DONE___'

pyglet.clock.schedule_interval(readInput, 0.01)

def ctrl_c_handler(signal, frame):
    pass
signal.signal(signal.SIGINT, ctrl_c_handler)

u = universe = Universe.Universe(sys.argv[1], json.loads(sys.argv[2][1:-1]))
w = universe.world
pyglet.app.run()
