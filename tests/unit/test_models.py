"""Unit tests for pwapi.models

Only methods with logic are tested. If logic exists in an init, the init is tested to see if the object serializes,
and if the given logic was executed properly. Simple attribute assignment is not tested. """

import pytest
from tests.stubs import nation_stub, nations_stub, members_stub
from pwapi.models import *


class TestNationsStub:
    # Testing init using data and different key names from the three different nation APIs
    def test_init_with_nation_data(self):
        data = nation_stub
        nation = NationsStub(data)
        assert nation.ruler == "Mikey"
        assert nation.nation == "Reach"
        assert nation.infrastructure == 22800
        assert not nation.vm

    def test_init_with_member_data(self):
        data = members_stub['nations'][0]
        nation = NationsStub(data)
        assert nation.ruler == "Luna"
        assert nation.nation == "Nightsilver Woods"
        assert nation.infrastructure == 17767.35
        assert nation.vm
