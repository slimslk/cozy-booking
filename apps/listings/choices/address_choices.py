from enum import Enum


class CountryChoices(Enum):
    ALBANIA = 'Albania'
    ANDORRA = 'Andorra'
    AUSTRIA = 'Austria'
    BELGIUM = 'Belgium'
    BOSNIA_AND_HERZEGOVINA = 'Bosnia_and_Herzegovina'
    BULGARIA = 'Bulgaria'
    CROATIA = 'Croatia'
    CYPRUS = 'Cyprus'
    CZECH = 'Czech'
    DENMARK = 'Denmark'
    ESTONIA = 'Estonia'
    FINLAND = 'Finland'
    FRANCE = 'France'
    GEORGIA = 'Georgia'
    GERMANY = 'Germany'
    GREECE = 'Greece'
    HUNGARY = 'Hungary'
    ICELAND = 'Iceland'
    IRELAND = 'Ireland'
    ITALY = 'Italy'
    KOSOVO = 'Kosovo'
    LATVIA = 'Latvia'
    LIECHTENSTEIN = 'Liechtenstein'
    LITHUANIA = 'Lithuania'
    LUXEMBOURG = 'Luxembourg'
    MALTA = 'Malta'
    MOLDOVA = 'Moldova'
    MONACO = 'Monaco'
    MONTENEGRO = 'Montenegro'
    NETHERLANDS = 'Netherlands'
    NORTH_MACEDONIA = 'North_Macedonia'
    NORWAY = 'Norway'
    POLAND = 'Poland'
    PORTUGAL = 'Portugal'
    ROMANIA = 'Romania'
    SAN_MARINO = 'San_Marino'
    SERBIA = 'Serbia'
    SLOVAKIA = 'Slovakia'
    SLOVENIA = 'Slovenia'
    SPAIN = 'Spain'
    SWEDEN = 'Sweden'
    SWITZERLAND = 'Switzerland'
    TURKEY = 'Turkey'
    UKRAINE = 'Ukraine'
    UNITED_KINGDOM = 'United_Kingdom'

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


    def __str__(self):
        return self.name


class LandChoice(Enum):
    NOT_IDENTIFIED = "Not identified"
    BADEN_WUERTTEMBERG = "Baden-Württemberg"
    BAVARIA = "Bayern"
    BERLIN = "Berlin"
    BRANDENBURG = "Brandenburg"
    BREMEN = "Bremen"
    HAMBURG = "Hamburg"
    HESSE = "Hessen"
    LOWER_SAXONY = "Niedersachsen"
    MECKLENBURG_VORPOMMERN = "Mecklenburg-Vorpommern"
    NORTH_RHINE_WESTPHALIA = "Nordrhein-Westfalen"
    RHINELAND_PALATINATE = "Rheinland-Pfalz"
    SAARLAND = "Saarland"
    SAXONY = "Sachsen"
    SAXONY_ANHALT = "Sachsen-Anhalt"
    SCHLESWIG_HOLSTEIN = "Schleswig-Holstein"
    THURINGIA = "Thüringen"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

    def __str__(self):
        return self.name
