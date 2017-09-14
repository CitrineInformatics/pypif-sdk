from os import environ
from citrination_client import CitrinationClient


def get_client(site=None):
    """Get a citrination client"""
    if 'CITRINATION_API_KEY' not in environ:
        raise ValueError("'CITRINATION_API_KEY' is not set as an environment variable")
    if not site:
        site = environ.get("CITRINATION_SITE", "https://citrination.com")
    return CitrinationClient(environ['CITRINATION_API_KEY'], site)

