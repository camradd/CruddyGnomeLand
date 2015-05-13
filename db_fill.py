import inspect

DENY = PULL = None

def connect(a):
    pass

def StringField():
    return None

def ReferenceField(name, reverse_delete_rule=None):
    return None

def DateTimeField(default=None):
    if inspect.isfunction(default) or inspect.isbuiltin(default):
        return default()
    else:
        return default

def ListField(t):
    return []

def DictField():
    return {}

def FloatField():
    return None

def IntField(default = None):
    return default

class Document(object):
    def __init__(self):
        pass
    def save(self):
        pass
