def mergeDict(destination, source):
    for key, value in source.iteritems():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            mergeDict(node, value)
        else:
            destination[key] = value
    return destination
