class Food:

    '''
    Food object. Has variable nutrition value, which is normally positive, but
    can be negative.
    '''

    def __init__(self):
        self.value = random.uniform(-1,10) #can be "posionous"

    def __repr__(self):
        return "f"

class Tree:

    '''
    Tree object, in world. Carries variable damage value.
    '''

    def __init__(self):
        self.value = random.uniform(-5,0)

    def __repr__(self):
        return "T"
