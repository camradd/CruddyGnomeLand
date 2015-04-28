import conx, math, random

class EvalNet(conx.BackpropNetwork):

    '''
    Evaluation Network. Inherited trait that does not change over the lifetime
    of the creature. The evaluation network takes as input four directions,
    each denoting what the creature sees in that direction, and what the
    creatures current health is. The evaluation network then outputs a real
    valued scalar.
    '''

    def __init__(self, weights = None, epsilon = 0.3, momentum = 0.9,
                    tolerance = 0.1):

        conx.BackpropNetwork.__init__(self)
        self.addLayers(5, 1)
        self.setEpsilon(epsilon)
        self.setMomentum(momentum)
        self.setTolerance(tolerance)



class ActNet(conx.SigmaNetwork):

    '''
    Action Network. Inherited trait that changes over the lifetime of the
    creature via reinforcement learning. The reinforcement learning algorithm
    rewards behaviours that lead to positive evalutation, from EvalNet, and
    punishes those with negative evaluation. The action network takes as input
    what the creature sees (in each direction) and the creature's health. The
    action network then outputs 5 bits, specifiying in which direction to move
    (the fifth bit allows the creature to stay) in a one hot representation.
    '''

    def __init__(self, weights = None, epsilon = 0.3, momentum = 0.9,
                    tolerance = 0.1):

        conx.SigmaNetwork.__init__(self)
        self.addLayers(5, 5)
        self.setEpsilon(epsilon)
        self.setMomentum(momentum)
        self.setTolerance(tolerance)

class Creature:

    '''
    Creature class. Each creature has an action network, determining what action
    the creature makes on any given turn, and an evaluation network, determining
    whether the action bettered or worsened the wellbeing of the creature.
    '''

    def __init__(self, genome = None):
        self.evalNet = EvalNet()
        self.actNet = ActNet()
        self.sight = [[]*4 for i in range(4)]
        self.health = 1.0

        if genome != None:
            self.genome =
                self.evalNet.getWeights("input", "output")
                self.actNet.getWeights("input", "output")

        else:
            self.genome = genome
            self.setWeights(genome)

    def __repr__(self):
        return "^_^"

    def initWeights(genome):
        #setWeight(self, fromName, fromPos, toName, toPos, value)
        for network in self.genome:
            for i in range(len(network)): # from node
                for j in range(len(network)): # to node
                    self.evalNet.setWeight("input", i,
                     "output",j, netWeights[weight])
