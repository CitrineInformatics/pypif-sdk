from os import environ
from citrination_client import CitrinationClient


def get_client(site='https://citrination.com'):
    """Get a citrination client"""
    if 'CITRINATION_API_KEY' not in environ:
        return None
    return CitrinationClient(environ['CITRINATION_API_KEY'], site)

