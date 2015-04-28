import conx, math, random

class EvalNet(conx.BackpropNetwork):

    '''
    Evaluation Network. Inherited trait that does not change over the lifetime
    of the creature. The evaluation network takes as input the closeness of
    landscape features, food, other creatures, etc in each of the four
    directions (within the visible distance),  creature's current health.
    The evaluation network then outputs a real valued scalar.
    '''

    def __init__(self, weights = None):
        conx.BackpropNetwork.__init__(self)
        self.addLayers(5, 1)
        self.setEpsilon(0.3)
        self.setMomentum(0.9)
        self.setTolerance(0.1)

class ActNet(conx.SigmaNetwork):

    '''
    Action Network. Inherited trait that changes over the lifetime of the
    creature via reinforcement learning. The reinforcement learning algorithm
    rewards behaviours that lead to positive evalutation, from EvalNet, and
    punishes those with negative evaluation (CBRP). The action network takes the
    same inputs as the EvalNet. The action network then outputs 5 probablilties,
    each one corresponding to a in which direction to move (the fifth one allows
    the creature to stay put) in a one hot representation.
    '''

    def __init__(self, weights = None):
        conx.SigmaNetwork.__init__(self)
        self.addLayers(5, 5)
        self.setEpsilon(0.3)
        self.setMomentum(0.9)
        self.setTolerance(0.1)

class Creature:

    '''
    Creature class. Each creature has an action network, determining what action
    the creature makes on any given turn, and an evaluation network, determining
    whether the action bettered or worsened the wellbeing of the creature.
    '''

    def __init__(self, genome = None):
        if genome != None:
            self.genome = self.evalNet.getWeights("input", "output") + \
                          self.actNet.getWeights("input", "output")
        else:
            self.genome = genome

        self.evalNet = EvalNet(genome[0])
        self.actNet = ActNet(genome[1])
        self.sight = [[]*4 for i in range(4)]
        self.health = 1.0

    def __repr__(self):
        return "^_^"

    def initWeights(genome):
        #setWeight(self, fromName, fromPos, toName, toPos, value)
        for network in self.genome:
            for i in range(len(network)): # from node
                for j in range(len(network)): # to node
                    self.evalNet.setWeight("input", i,
                     "output",j, netWeights[weight])
