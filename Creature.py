import TileObject, conx, math, random, numpy, uuid

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

class Creature(TileObject.TileObject):

    '''
    Creature class. Each creature has an action network, determining what action
    the creature makes on any given turn, and an evaluation network, determining
    whether the action bettered or worsened the wellbeing of the creature.
    '''

    visibilityIndex = 10


    def __init__(self, genome = None):
        self.evalNet = EvalNet()
        self.actNet = ActNet()
        self.health = 1.0
        self.tile = None
        self.lastAction = None
        self.seeds = str(self.evalNet.seed) + str(self.actNet.seed)
        self.id = uuid.uuid4()
        self.age = 0
        self.parents = []
        self.children = []


        if genome == None:
            evalWeights = self.evalNet.getWeights("input", "output").flatten().tolist()
            actWeights = self.actNet.getWeights("input", "output").flatten().tolist()
            self.genome = evalWeights + actWeights

        else:
            evalWeightSize = self.evalNet.inputSize * self.evalNet.outputSize
            self.genome = genome
            self.setWeights(self.evalNet, self.genome[0:evalWeightSize])
            self.setWeights(self.actNet, self.genome[evalWeightSize:])

    @property
    def sight(self):
        return self.world.getSight(self)

    @property
    def world(self):
        return None if self.tile == None else self.tile.world


    def __repr__(self):
        return "^_^"
        return "p" + "".join(self.parents + "c" self.children

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
        self.world.dead += 1
        self.tile.removeTileObject(self)

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


    def reproduce(self, orgy = True, mutateGene = False):
        self.world.born += 1
        nearby = self.world.getNearbyCreatures(self)
        kid = None
        if len(nearby) == 0:
            kid = Creature(self.mutate(self.genome), mutateGene)
            kid.parents = [self.id]
        else:
            if orgy == True:
                parents = [p.genome for p in nearby + [self]]
                while len(parents) > 1:
                    p1 = random.choice(parents)
                    parents.remove(p1)
                    p2 = random.choice(parents)
                    parents.remove(p2)
                    parents.append(self.crossover(p1,p2))
                kid = Creature(self.mutate(parents[0], mutateGene))
                kid.parents = [p.id for p in nearby + [self]]
            else:
                kid = self.mutate(self.crossover(random.choice(nearby).genome, \
                                  self.genome), mutateGene)
        self.children.append(kid.id)
        return kid

    def mutate(self, genome, rate = .3, mutateGene):
        if mutateGene:
            return [
                g + random.uniform(-.5,.5) if random.uniform(0,1) < rate else \
                g for g in genome
            ]
        else: return genome

    def crossover(self, mateGenome, partnerGenome):
        pivot = random.choice(range(len(mateGenome)))
        return [mateGenome[i] if i < pivot else partnerGenome[i] for i in range(len(mateGenome))]
