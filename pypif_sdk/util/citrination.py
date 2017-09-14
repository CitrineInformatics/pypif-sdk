from os import environ
from citrination_client import CitrinationClient


def get_client(site=None):
    """Get a citrination client"""
    if 'CITRINATION_API_KEY' not in environ:
        return None
    if not site:
        site = environ.get("CITRINATION_SITE", "https://citrination.com")
    return CitrinationClient(environ['CITRINATION_API_KEY'], site)

