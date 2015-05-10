import atexit, sys, json
import subprocess as sp

runs = {}

def run(name, settings = {}):
    if name in runs:
        print 'Run with that name already exists!'
        return

    r = sp.Popen(['python', '_run_process.py', name, "'" + json.dumps(settings) + "'"],
                    stderr=sp.PIPE, stdout=sp.PIPE, # comment this out to see errors in outer shell
                    stdin=sp.PIPE)
    runs[name] = r

def kill(name):
    if not (name in runs):
        print 'No run with that name already exists!'
        return

    runs[name].kill()

def enter(name):
    if not (name in runs):
        print 'No run with that name already exists!'
        return

    p = runs[name]
    out = p.stdout

    print 'Entering universe "' + name + '". Type "exit" to leave. Variable u and w are the ' + \
          'unvierse and world respectively.'

    while 1:
        s = raw_input(name + ' -> ')
        if s == 'exit':
            return
        print >> p.stdin, s

        while 1:
            o = out.readline()
            if o == '___DONE___\n':
                break
            print o,

@atexit.register
def on_exit():
    for p in runs.values():
        p.kill()

print 'Welcome to Cruddy Gnome Land!'

if not sys.flags.interactive:
    print 'Run this file interactively (python -i ' + sys.argv[0] + ').'
    sys.exit()

h  = 'run("<name>"[, settings]) = start a new universe\n'
h += 'enter("<name>")           = enter universe'
print h
