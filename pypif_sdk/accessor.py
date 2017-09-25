

def get_propety_by_name(pif, name):
    """Get a property by name"""
    return next((x for x in pif.properties if x.name == name), None)
