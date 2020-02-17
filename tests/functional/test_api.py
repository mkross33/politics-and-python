"""Unit tests for api.py"""
from pwapi.api import *
from unittest.mock import patch
import requests
import requests_mock


@patch("requests.get")
def test_nation_with_valid_id_returns_object(get_mock):
    mikey = get_nation(31191)
    assert mikey.nation_id == 31191

