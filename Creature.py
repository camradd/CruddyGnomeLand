import conx, math, random, numpy

class EvalNet(conx.BackpropNetwork):

    '''
    Evaluation Network. Inherited trait that does not change over the lifetime
    of the creature. The evaluation network takes as input the closeness of
    landscape features, food, other creatures, etc in each of the four
    directions (within the visible distance),  creature's current health.
    The evaluation network then outputs a real valued scalar.
    '''

    def __init__(self):
        conx.BackpropNetwork.__init__(self)
        self.inputSize = 5
        self.outputSize = 1
        self.addLayers(self.inputSize, self.outputSize)
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

    def __init__(self):
        conx.SigmaNetwork.__init__(self)
        self.inputSize = 5
        self.outputSize = 5
        self.addLayers(self.inputSize, self.outputSize)
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
        self.evalNet = EvalNet()
        self.actNet = ActNet()
        self.sight = [[]*4 for i in range(4)]
        self.health = 1.0

        if genome == None:
            self.evalWeights = \
                self.evalNet.getWeights("input", "output").flatten().tolist()
            self.actWeights = \
                self.actNet.getWeights("input", "output").flatten().tolist()
            self.genome = self.evalWeights + self.actWeights

        else:
            evalWeightSize = self.evalNet.inputSize * self.evalNet.outputSize
            self.genome = genome
            self.evalWeights = self.genome[0:evalWeightSize]
            self.actWeights = self.genome[evalWeightSize:]

        self.setWeights(self.evalNet, self.evalWeights)
        self.setWeights(self.actNet, self.actWeights)

    def __repr__(self):
        return "^_^"

    def setWeights(self, net, weights):
        #setWeight(self, fromName, fromPos, toName, toPos, value)
        index = 0
        for i in range(net.inputSize): # from node
            for o in range(net.outputSize): # to node
                net.setWeight("input", i,"output", o, weights[index])
                index += 1
