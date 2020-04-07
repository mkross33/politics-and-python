"""Implements the pwapi API"""
from .models import *
from pwapi.requests import call_api

# optional default key for all API call, to be set by end user as necessary
default_key = None
pw_url = "http://politicsandwar.com"
pw_api = f"{pw_url}/api"


def get_nation(nation_id: int, key=default_key) -> object:
    """Creates a nation object for a given ID"""
    url = f"{pw_api}/nation/id={nation_id}&key={key}"
    data = call_api(url)
    new_nation = Nation(data)
    return new_nation
