import TileObject, conx, math, random, numpy, merge

# try:
#     import mongoengine as db
# except ImportError:
#     import db_fill as db
import db_fill as db

class EvalNet(conx.BackpropNetwork):

    '''
    Evaluation Network. Inherited trait that does not change over the lifetime
    of the creature. The evaluation network takes as input the closeness of
    landscape features, food, other creatures, etc in each of the four
    directions (within the visible distance), and  creature's current health.
    These result in 13 inputs. The evaluation network then outputs a real valued
    scalar.
    '''

    def __init__(self):
        conx.BackpropNetwork.__init__(self)
        self.inputSize = 13
        self.outputSize = 1
        self.addLayers(self.inputSize, self.outputSize)
        self.setEpsilon(0.3)
        self.setMomentum(0.9)
        self.setTolerance(0.1)

class ActNet(conx.BackpropNetwork):

    '''
    Action Network. Inherited trait that changes over the lifetime of the
    creature via reinforcement learning. The reinforcement learning algorithm
    rewards behaviours that lead to positive evalutation, from EvalNet, and
    punishes those with negative evaluation (CBRP). The action network takes the
    same inputs as the EvalNet. The action network then outputs 5 probablilties,
    each one corresponding to a in which direction to move (the fifth one allows
    the creature to stay put) in a one hot representation.
    '''

    def __init__(self):
        conx.BackpropNetwork.__init__(self)
        self.log = False
        self.inputSize = 13
        self.outputSize = 2
        self.addLayers(self.inputSize, self.outputSize)
        self.setEpsilon(0.3)
        self.setMomentum(0.9)
        self.setTolerance(0.1)

    def Print(self, str): pass

class Creature(TileObject.TileObject, db.Document):

    '''
    Creature class. Each creature has an action network, determining what action
    the creature makes on any given turn, and an evaluation network, determining
    whether the action bettered or worsened the wellbeing of the creature.
    '''

    visibilityIndex = 10

    health = db.FloatField()
    age = db.IntField()
    genome = db.ListField(db.FloatField())
    parents = db.ListField(db.ReferenceField('self', reverse_delete_rule=db.PULL))
    generation = db.IntField(default = 0)
    timeBorn = db.IntField(default = 0)
    actWeights = db.ListField(db.FloatField())

    def __init__(self, genome = None, settings = {}):
        db.Document.__init__(self)
        TileObject.TileObject.__init__(self)

        defaultSettings = {
            'orgy': True,
            'mutationRate': 0.3,
            'minMutation': -0.5,
            'maxMutation': 0.5,
            'inheritLearntWeights': False
        }
        self.settings = merge.mergeDict(defaultSettings, settings)

        self.evalNet = EvalNet()
        self.actNet = ActNet()
        self.lastAction = None

        self.health = 1.0
        self.age = 0

        if genome == None and len(self.genome) == 0:
            evalWeights = self.evalNet.getWeights("input", "output").flatten().tolist()
            actWeights = self.actNet.getWeights("input", "output").flatten().tolist()
            self.genome = evalWeights + actWeights

        else:
            evalWeightSize = self.evalNet.inputSize * self.evalNet.outputSize
            if len(self.genome) == 0: self.genome = genome
            self.setWeights(self.evalNet, self.genome[0:evalWeightSize])
            if len(self.actWeights) != 0:
                self.setWeights(self.actWeights)
            else:
                self.setWeights(self.actNet, self.genome[evalWeightSize:])

        self.save()

    def clean(self):
        self.actWeights = self.actNet.getWeights("input", "output").flatten().tolist()

    @property
    def sight(self):
        return self.world.getSight(self)

    @property
    def tile(self):
        return self._tile
    @tile.setter
    def tile(self, tile):
        self._tile = tile
        self.world = (None if tile == None else tile.world)

    def setWeights(self, net, weights):
        index = 0
        for i in range(net.inputSize): # from node
            for o in range(net.outputSize): # to node
                net.setWeight("input", i,"output", o, weights[index])
                index += 1

    def effect(self, creature):
        r = 0
        if creature.health * random.uniform(0,2) > self.health:
            r = -creature.health * random.uniform(.1,.5)
        else:
            r = creature.health * random.uniform(.3,1)
        self.lastEffect = r
        return r

    def canEnter(self, creature):
        r = False if self.lastEffect < 0 else True
        if r == True:
            self.die()
        return r

    def changeHealth(self, delta):
        self.health = max(min(self.health + delta, 1), 0)
        if self.health == 0:
            self.die()

    def die(self):
        if self.tile == None: return
        self.save()
        self.world.removeCreature(self)

    def makeAction(self):
        probs = self.actNet.propagate(input = self.sight + [self.health])
        action = [1 if p > random.uniform(0,1) else 0 for p in probs]
        return action

    def step(self):
        self.age += 1
        self.lastInput = self.sight + [self.health]
        self.lastEval = self.evalNet.propagate(input = self.lastInput)
        self.lastAction = self.makeAction()
        self.world.act(self, self.lastAction)
        self.changeHealth(-.0005)

        if self.health > 0 and random.uniform(0,1) < .002:
            self.world.spawnCreature(self.reproduce())

    def stepFinished(self):
        if self.lastAction == None: return
        newEval = self.evalNet.propagate(input = self.sight + [self.health])
        targets = self.lastAction
        if newEval < self.lastEval:
            targets = [0 if o == 1 else 1 for o in targets]
        self.actNet.setInputs([self.lastInput])
        self.actNet.setTargets([targets])
        self.actNet.train(1)

    def reproduce(self):
        nearby = self.world.getNearbyCreatures(self)
        c = None
        if len(nearby) == 0:
            c = Creature(self.mutate(self.genome), self.settings)
            c.generation = self.generation + 1
            c.parents.append(self)
        else:
            if self.settings['orgy']:
                parents = [p.genome for p in nearby + [self]]
                while len(parents) > 1:
                    p1 = random.choice(parents)
                    parents.remove(p1)
                    p2 = random.choice(parents)
                    parents.remove(p2)
                    parents.append(self.crossover(p1,p2))
                c = Creature(self.mutate(parents[0]), self.settings)
                for p in nearby + [self]: c.parents.append(p)
                c.generation = max([p.generation for p in nearby + [self]])

            else:
                parent2 = random.choice(nearby)
                genome = self.mutate(self.crossover(parent2.genome, self.genome))
                c = Creature(genome, self.settings)
                c.parents.append(self)
                c.parents.append(parent2)
                c.generation = max([self.generation, parent2.generation])

        c.timeBorn = self.world.time
        return c

    def mutate(self, genome):
        rate = self.settings['mutationRate']
        minD, maxD = self.settings['minMutation'], self.settings['maxMutation']
        return [
            g + random.uniform(minD, maxD) if random.uniform(0,1) < rate else g for g in genome
        ]

    def crossover(self, mateGenome, partnerGenome):
        pivot = random.choice(range(len(mateGenome)))
        return [
            mateGenome[i] if i < pivot else \
            partnerGenome[i] for i in range(len(mateGenome))
        ]
