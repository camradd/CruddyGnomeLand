import Universe, sys, pyglet, signal, time
from AsyncFIFORead import AsyncFIFORead

f = AsyncFIFORead(sys.stdin)

def readInput(dx):
    line = f.readline()
    if line == None: return
    try:
        exec line in globals(), globals()
    except Exception as e:
        print e
    print '___DONE___'

pyglet.clock.schedule_interval(readInput, 0.1)

def ctrl_c_handler(signal, frame):
    pass
signal.signal(signal.SIGINT, ctrl_c_handler)

universe = Universe.Universe(sys.argv[1])
pyglet.app.run()
