from warnings import warn

def get_propety_by_name(pif, name):
    """Get a property by name"""
    warn("This method has been deprecated in favor of get_property_by_name")
    return next((x for x in pif.properties if x.name == name), None)

def get_property_by_name(pif, name):
    """Get a property by name"""
    return next((x for x in pif.properties if x.name == name), None)