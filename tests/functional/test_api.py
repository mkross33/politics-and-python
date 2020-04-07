"""Integration tests for api.py. These also act as functional tests for the apps public contract."""
import pytest
from pwapi.api import *
from pwapi.exceptions import *
from pwapi.models import Nation
from tests.stubs import *
import os

key = os.getenv("PW_KEY")


class TestNation:
    """All tests relating to public API for creating and using Nation objects"""
    def test_invalid_id_throws_exception(self):
        # the nation with ID 1 has been deleted, and IDs are never reused, so it is safe to use this to always return
        # a non-existant nation error
        with pytest.raises(InvalidRequest):
            no_nation = get_nation(1, key)

    def test_get_nation_creates_new_object(self):
        mikey = get_nation(31191, key)
        assert isinstance(mikey, object)
        assert mikey.nation_id == 31191
        assert mikey.ruler == "Mikey"

    def test_get_wars_with_no_wars_leaves_empty_list(self):
        mikey = Nation(nation_stub)
        mikey.get_wars()
        assert mikey.wars == {"offensive": [], "defenisve": []}
