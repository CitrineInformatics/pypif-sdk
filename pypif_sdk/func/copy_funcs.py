import pypif


def copy(pif):
    """
    Copy a pif

    :param pif: pif object to copy
    """
    return pypif.pif.loads(pypif.pif.dumps(pif))
