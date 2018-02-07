from os import environ
from citrination_client import CitrinationClient
from pypif.pif import dumps


def get_client(site=None):
    """Get a citrination client"""
    if 'CITRINATION_API_KEY' not in environ:
        raise ValueError("'CITRINATION_API_KEY' is not set as an environment variable")
    if not site:
        site = environ.get("CITRINATION_SITE", "https://citrination.com")
    return CitrinationClient(environ['CITRINATION_API_KEY'], site)


def set_uids(pifs, uids=None):
    """
    Set the uids in a PIF, explicitly if the list of UIDs is passed in
    :param pifs: to set UIDs in
    :param uids: to set; defaults to a hash of the object
    :return:
    """
    if not uids:
        uids = [str(hash(dumps(x))) for x in pifs]
    for pif, uid in zip(pifs, uids):
        pif.uid = uid
    return pifs


def get_url(pif, dataset, version=1, site="https://citrination.com"):
    """
    Construct the URL of a PIF on a site
    :param pif: to construct URL for
    :param dataset: the pif will belong to
    :param version: of the PIF (default: 1)
    :param site: for the dataset (default: https://citrination.com)
    :return: the URL as a string
    """
    return "{site}/datasets/{dataset}/version/{version}/pif/{uid}".format(
        uid=pif.uid, version=version, dataset=dataset, site=site
    )

