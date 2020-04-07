
def militarization(city_count, soldiers, tanks, aircraft, ships):
    """Calculates militarization levels of each unit type, and for all units in total"""
    soldiers_per_barracks = 3000
    barracks_per_city = 5
    tanks_per_factory = 250
    factories_per_city = 5
    aircraft_per_hanger = 18
    hangers_per_city = 5
    ships_per_dock = 5
    docks_per_city = 3

    max_soldiers = soldiers_per_barracks * barracks_per_city * city_count
    max_tanks = tanks_per_factory * factories_per_city * city_count
    max_aircraft = aircraft_per_hanger * hangers_per_city * city_count
    max_ships = ships_per_dock * docks_per_city * city_count

    ratio = {"total": None,
                "soldiers": soldiers / max_soldiers,
                "tanks": tanks / max_tanks,
                "aircraft": aircraft / max_aircraft,
                "ships": ships / max_ships}

    ratio["total"] = (ratio["soldiers"] + ratio["tanks"] + ratio["aircraft"] + ratio["ships"]) / 4

    return ratio


def war_range(score):
    offensive = {"max": score * 1.75,
                 "min": score * .75}
    defensive = {"max": score / .75,
                 "min": score / 1.75}

    return {"offensive": offensive, "defensive": defensive}
