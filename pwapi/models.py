""" Classes representing game objects returned by the various APIs

Classes
--------

NationsStub - individual nation data from Nations API
BaseNation - Parent class for Nation and Member
Nation - represents in-game nation from Nation API Data
Member - represents a member nation from the Alliance_Member API
CompleteMember - Combines Nation and Member class to provide all accessible nation data
"""

from pwapi import formulas


class NationStub:
    """Representation of Nations API data

    The NationStub object contains the parameters returned for each nation by the PW Nations API. This API returns a
    stub of the data covered in the Nation API and Alliance_Members API, and is thus used as a parent class for both

    Methods
    -------------

    war_range: returns a dictionary containing the offensive and defensive war ranges for the nation"""

    __slots__ = ["nation_id", "nation_name", "leader_name", "war_policy", "color", "alliance_name", "alliance_id",
                 "alliance_position", "city_count", "infrastructure", "offensive_war_count", "defensive_war_count",
                 "score", "vacation_mode", "minutes_inactive"]

    def __init__(self, data: dict):
        """Init with API data

        Args:
            :param data (dict): Dictionary containing nation data from the Nations, Nation, or Alliance_Members API"""

        # The Nation API returns several shared attributes with different types, and sometimes different names,
        # than are used in Nations or Alliance_Members. Hence retyping or logic looking for specific keys
        self.nation_id = int(data['nationid'])
        if "nation" in data:
            self.nation_name = data["nation"]
        else:
            self.nation_name = data["name"]
        if "leadername" in data:
            self.leader_name = data["leadername"]
        else:
            self.leader_name = data["leader"]
        self.war_policy = data["war_policy"]
        self.color = data["color"]
        self.alliance_name = data["alliance"]
        self.alliance_id = int(data["allianceid"])
        self.alliance_position = int(data["allianceposition"])
        self.city_count = data["cities"]
        if "infrastructure" in data:
            self.infrastructure = float(data["infrastructure"])
        else:
            self.infrastructure = float(data["totalinfrastructure"])
        self.offensive_war_count = data["offensivewars"]
        self.defensive_war_count = data["defensivewars"]
        self.score = float(data["score"])
        if "vacmode" in data:
            self.vacation_mode = bool(int(data["vacmode"]))
        else:
            self.vacation_mode = bool(int(data["vmode"]))
        self.minutes_inactive = data["minutessinceactive"]

    def war_range(self):
        """Returns the war range for this nation

        return: A dictionary of war ranges. Keys: offensive, defensive. Each is its own dict with keys max, min
        representing the war range"""
        offensive = {"max": self.score * 1.75,
                     "min": self.score * .75}
        defensive = {"max": self.score / .75,
                     "min": self.score / 1.75}

        return {"offensive": offensive, "defensive": defensive}


class BaseNation(NationStub):
    """Parent class of Nation and Member, holding additional shared attributes

    BaseNation extends NationsStub with more attributes shared between Nation and Alliance_Members API endpoints, but
    which are not included in Nations."""

    __slots__ = ["soldiers", "tanks", "aircraft", "ships", "missiles", "nukes", "projects"]

    def __init__(self, data: dict):
        """Init with API data

        :param data (dict): dictionary of nation data from Nation or Alliance_Members API

        Methods
        ------------------

        militarization - returns a dictionary of militarization levels"""

        super(BaseNation, self).__init__(data)
        # Nation API returns military values as strings
        self.soldiers = int(data["soldiers"])
        self.tanks = int(data["tanks"])
        self.aircraft = int(data["aircraft"])
        self.ships = int(data["ships"])
        self.missiles = int(data["missiles"])
        self.nukes = int(data["nukes"])
        # Nation API bizarrely returns project booleans as strings of ints
        self.projects = {"bw": bool(int(data["bauxiteworks"])),
                         "iw": bool(int(data["ironworks"])),
                         "as": bool(int(data["armsstockpile"])),
                         "egr": bool(int(data["emgasreserve"])),
                         "mi": bool(int(data["massirrigation"])),
                         "itc": bool(int(data["inttradecenter"])),
                         "mlp": bool(int(data["missilelpad"])),
                         "nrf": bool(int(data["nuclearresfac"])),
                         "id": bool(int(data["irondome"])),
                         "vds": bool(int(data["vitaldefsys"])),
                         "uep": bool(int(data["uraniumenrich"])),
                         "ia": bool(int(data["intagncy"])),
                         "pb": bool(int(data["propbureau"])),
                         "cce": bool(int(data["cenciveng"]))}

    def militarization(self):
        """ Calculates the nation's militarization levels

        return: a dictionary of militarization levels for the nation overall plus each unit type. Keys: (soldiers,
        tanks, aircraft, ships, total). Values are calculated as fractions and are NOT converted to percentages."""
        return formulas.militarization(self.city_count, self.soldiers, self.tanks, self.aircraft, self.ships)


class Nation(BaseNation):
    """ Object representing a PW Nation as given by the Nation API"""

    __slots__ = ["nation_title", "continent", "social_policy", "unique_id", "government", "domestic_policy",
                 "date_created",
                 "days_old", "flag_url", "ruler_title", "economic_policy", "approval_rating", "nation_rank", "city_ids",
                 "cities", "latitude", "longitude", "population", "gdp", "land", "soldiers_lost", "soldiers_killed",
                 "tanks_lost", "tanks_killed", "aircraft_lost", "aircraft_killed", "ships_lost", "ships_killed",
                 "missiles_launched", "missiles_eaten", "nukes_launched", "nukes_eaten", "infrastructure_destroyed",
                 "infrastructure_lost", "money_looted", "offensive_war_ids", "defensive_war_ids", "beige_turns",
                 "radiation", "season", "espionage_available", "wars"]

    def __init__(self, data: dict):
        super(Nation, self).__init__(data)
        self.nation_title = data["prename"]
        self.continent = data["continent"]
        self.social_policy = data["socialpolicy"]
        self.unique_id = data["uniqueid"]
        self.government = data["government"]
        self.domestic_policy = data["domestic_policy"]
        self.date_created = data["founded"]
        self.days_old = data["daysold"]
        self.flag_url = data["flagurl"]
        self.ruler_title = data["title"]
        self.economic_policy = data["ecopolicy"]
        self.approval_rating = data["approvalrating"]
        self.nation_rank = data["nationrank"]
        self.city_ids = [int(city_id) for city_id in data["cityids"]]
        # Dict to store related city objects that may be created. Key = city name.
        self.cities = {}
        # Dict to store list of war objects
        self.wars = {"offensive": [], "defensive": []}
        self.land = data["landarea"]
        # All of the following numeric attributes are returned by the API as strings
        self.latitude = float(data["latitude"])
        self.longitude = float(data["longitude"])
        self.population = int(data["population"])
        self.gdp = float(data["gdp"])
        self.soldiers_lost = int(data["soldiercasualties"])
        self.soldiers_killed = int(data["soldierskilled"])
        self.tanks_lost = int(data["tankcasualties"])
        self.tanks_killed = int(data["tankskilled"])
        self.aircraft_lost = int(data["aircraftcasualties"])
        self.aircraft_killed = int(data["aircraftkilled"])
        self.ships_lost = int(data["shipcasualties"])
        self.ships_killed = int(data["shipskilled"])
        self.missiles_launched = int(data["missilelaunched"])
        self.missiles_eaten = int(data["missileseaten"])
        self.nukes_launched = int(data["nukeslaunched"])
        self.nukes_eaten = int(data["nukeseaten"])
        self.infrastructure_destroyed = float(data["infdesttot"])
        self.infrastructure_lost = float(data["infraLost"])
        self.money_looted = float(data["moneyLooted"])
        self.offensive_war_ids = [int(war_id) for war_id in data["offensivewar_ids"]]
        self.defensive_war_ids = [int(war_id) for war_id in data["defensivewar_ids"]]
        self.beige_turns = data["beige_turns_left"]
        self.radiation = data["radiation_index"]
        self.season = data["season"]
        self.espionage_available = data["espionage_available"]

    def get_wars(self):
        offensive = []
        for war_id in self.offensive_war_ids:
            war = get_war(war_id)
            offensive.append(war)
        defensive = []
        for war_id in self.defensive_war_ids:
            war = get_war(war_id)
            defensive.append(war)


class Member(BaseNation):
    """ Object representing a member nation, as given by the alliance_members API """

    # Due to multiple inheritence issues with subclass CompleteMember, this class cannot use slots.

    # *args represents the optional dict for nation API data, passed into Nation class as part of the multiple
    # inheritence chain of CompleteMember
    def __init__(self, data, *args: dict):
        # Different data is sent to different parent classes depending on if this is being instantiated, or called as
        # a super class
        if args:
            super(Member, self).__init__(*args)
        else:
            super(Member, self).__init__(data)
        self.city_cooldown = data['cityprojecttimerturns']
        # all numerical values are returned by the API as strings
        self.money = float(data["money"])
        self.food = float(data["food"])
        self.uranium = float(data["uranium"])
        self.coal = float(data["coal"])
        self.oil = float(data["oil"])
        self.bauxite = float(data["bauxite"])
        self.lead = float(data["lead"])
        self.iron = float(data["iron"])
        self.gasoline = float(data["gasoline"])
        self.munitions = float(data["munitions"])
        self.aluminum = float(data["aluminum"])
        self.steel = float(data["steel"])
        self.credits = float(data["credits"])
        self.spies = float(data["spies"])


class CompleteMember(Member, Nation):
    """ Representation of all available data about a nation, combining Nation API and members API data."""

    def __init__(self, member_data, nation_data):
        super(CompleteMember, self).__init__(member_data, nation_data)


class War:
    """Object representing a PW War, as returned by the game's Wars API"""

    __slots__ = ["war_id", "ongoing", "start_date", "attacker_id", "attacker_alliance", "attacker_is_applicant",
                 "defender_id", "defender_alliance", "defender_is_applicant", "attacker_offering_peace", "war_reason",
                 "ground_control"]

    def __init__(self, data, war_id):
        # The War API is bugged to always return war_id as 0, so it gets passed in by the get_war function instead
        self.war_id: int = war_id
        self.ongoing = data["war_ended"]
        self.start_date = data["date"]
        self.attacker_id = data["aggressor_id"]
        self.attacker_alliance = data["aggressor_alliance"]
        self.attacker_is_applicant = data["aggressor_is_applicant"]
        self.defender_id = data["defender_id"]
        self.attacker_offering_peace = data["aggressor_offering_peace"]
        self.ground_control = data["ground_control"]
