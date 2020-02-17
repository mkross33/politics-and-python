""" Classes representing game objects returned by the various APIs

Every attribute that is retyped within a class will have a comment noting the original bad return type, and where
applicable, which API returned it

Classes
--------

NationsStub - individual nation data from Nations API
BaseNation - Parent class for Nation and Member
Nation - represents in-game nation from Nation API Data
Member - represents a member nation from the Alliance_Member API
MemberComplete - Combines Nation and Member class to provide all accessible nation data
"""


class NationsStub:
    """Representation of Nations API data

    The NationStub object contains the parameters returned for each nation by the PW Nations API. This API returns a
    stub of the data covered in the Nation API and Alliance_Members API, and is thus used as a parent class for both """

    __slots__ = ["nation_id", "nation", "ruler", "war_policy", "color", "alliance", "alliance_id", "alliance_position",
                 "city_count", "infrastructure", "offensive_war_count", "defensive_war_count", "score", "vacation_mode",
                 "minutes_inactive"]

    def __init__(self, data: dict):
        """Init with API data

        Args:
            :param data (dict): Dictionary containing nation data from the Nations, Nation, or Alliance_Members API"""

        # The Nation API returns several shared attributes with different types, and sometimes different names,
        # than are used in Nations or Alliance_Members. Hence retyping or logic looking for specific keys
        self.nation_id = int(data['nationid'])
        if "nation" in data:
            self.nation = data["nation"]
        else:
            self.nation = data["name"]
        if "leadername" in data:
            self.ruler = data["leadername"]
        else:
            self.ruler = data["leader"]
        self.war_policy = data["war_policy"]
        self.color = data["color"]
        self.alliance = data["alliance"]
        self.alliance_id = int(data["allianceid"])
        self.alliance_position = int(data["allianceposition"])
        self.city_count = data["cities"]
        if "infrastructure" in data:
            self.infrastructure = int(data["infrastructure"])
        else:
            self.infrastructure = data["totalinfrastructure"]
        self.offensive_war_count = data["offensivewars"]
        self.defensive_war_count = data["defensivewars"]
        self.score = float(data["score"])
        if "vacmode" in data:
            self.vacation_mode = bool(int(data["vacmode"]))
        else:
            self.vacation_mode = bool(int(data["vmode"]))
        self.minutes_inactive = data["minutessinceactive"]


class BaseNation(NationsStub):
    """Base class holding shared attributes between Nation and Alliance_Members API objects

    BaseNation extends NationsStub, which contains some, but not all, of the attributes common to Nation and Member"""

    __slots__ = ["soldiers", "tanks", "aircraft", "ships", "missiles", "nukes", "projects"]

    def __init__(self, data: dict):
        """Init with API data

        :param data (dict): dictionary of nation data from Nation or Alliance_Members API"""

        super(BaseNation, self).__init__(data)
        # Nation API returns military values as strings
        self.soldiers = int(data["soldiers"])
        self.tanks = int(data["tanks"])
        self.aircraft = int(data["aircraft"])
        self.ships = int(data["ships"])
        self.missiles = int(data["missiles"])
        self.nukes = int(data["nukes"])
        # Nation API bizarrely returns project booleans as strings of ints
        self.projects = {"bauxiteworks": bool(int(data["bauxiteworks"])),
                         "ironworks": bool(int(data["ironworks"])),
                         "arms_stockpile": bool(int(data["armsstockpile"])),
                         "emergency_gasoline_reserve": bool(int(data["emgasreserve"])),
                         "mass_irrigation": bool(int(data["massirrigation"])),
                         "international_trade_center": bool(int(data["inttradecenter"])),
                         "missile_launch_pad": bool(int(data["missilepad"])),
                         "nuclear_research_facility": bool(int(data["nuclearresfac"])),
                         "iron_dome": bool(int(data["irondome"])),
                         "vital_defense_system": bool(int(data["vitaldefsys"])),
                         "uranium_enrichment_program": bool(int(data["uraniumenrich"])),
                         "intelligence_agency": bool(int(data["intagncy"])),
                         "propaganda_bureau": bool(int(data["propbureau"])),
                         "center_for_civil_engineering": bool(int(data["cenciveng"]))}


class Nation(BaseNation):
    """ Object representing a PW Nation as given by the Nation API"""

    __slots__ = ["title", "continent", "social_policy", "unique_id", "government", "domestic_policy", "date_created",
                 "days_old", "flag_url", "ruler_title", "economic_policy", "approval_rating", "nation_rank", "city_ids",
                 "cities", "latitude", "longitude", "population", "gdp", "land", "soldiers_lost", "soldiers_killed",
                 "tanks_lost", "tanks_killed", "aircraft_lost", "aircraft_killed", "ships_lost", "ships_killed",
                 "missiles_launched", "missiles_eaten", "nukes_launched", "nukes_eaten", "infrastructure_destroyed",
                 "infrastructure_lost", "money_looted", "offensive_war_ids", "defensive_war_ids", "beige_turns",
                 "radiation", "season", "espionage_available", "wars"]

    def __init__(self, data: dict):
        super(Nation, self).__init__(data)
        self.title = data["prename"]
        self.continent = data["continent"]
        self.social_policy = data["socialpolicy"]
        self.unique_id = data["uiqueid"]
        self.government = data["government"]
        self.domestic_policy = data["domestic_policy"]
        self.date_created = data["founded"]
        self.days_old = data["daysold"]
        self.flag_url = data["flagurl"]
        self.ruler_title = data["title"]
        self.economic_policy = data["ecopolicy"]
        self.approval_rating = data["approvalrating"]
        self.nation_rank = data["nationrank"]
        self.city_ids = data["cityids"]
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
        self.tanks_lost = int(data["tankcasualites"])
        self.tanks_killed = int(data["tankskilled"])
        self.aircraft_lost = int(data["aircraftcasualties"])
        self.aircraft_killed = int(data["aircraftkilled"])
        self.ships_lost = int(data["shipcasulaties"])
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
