import pytest
from pwapi.formulas import *


def test_militarization():
    mil_soldiers = 1/300
    mil_tanks = 1
    mil_aircraft = 1/50
    mil_ships = 1/10
    mil_total = (mil_soldiers + mil_tanks + mil_aircraft + mil_ships) / 4
    mil = militarization(city_count=10, soldiers=500, tanks=12500, aircraft=18, ships=15)
    assert mil == {"total": mil_total, "soldiers": mil_soldiers, "tanks": mil_tanks, "aircraft": mil_aircraft,
                   "ships": mil_ships}