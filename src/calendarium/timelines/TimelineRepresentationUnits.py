from enum import Enum

# class syntax
class TimelineRepresentationUnits(Enum):
    Second = 1
    Kilosecond = 1e3
    Megasecond = 1e6
    Gigasecond = 1e9
    Terasecond = 1e12
    Petasecond = 1e12
    Exasecond = 1e15
    Minute = 60
    Hour = 3600
    Day = 86400
    Week = 604800
    Month = 2629746
    Year = 31556952
    Julian_Year = 31557600
    Olympiad = 126227808
    Century = 3155695200
    Millenia = 31556952000
    Million_Years = 31556952000000
    Billion_Years = 31556952000000000
    Trillion_Years = 31556952000000000000