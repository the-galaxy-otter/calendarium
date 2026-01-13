from enum import Enum
from timeline import Timeline

# Default measurement units for Timespots
class TimespotUnit(Enum):
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    YEAR = 31556952
    JULIAN_YEAR = 31557600
    DECADE = 315569520
    CENTURY = 3155695200
    MILLENNIUM = 31556952000
    KILOSECOND = 1000
    MEGASECOND = 1000000
    GIGASECOND = 1000000000
    TERASECOND = 1000000000000
    KILOMINUTE = 60000
    MEGAMINUTE = 60000000
    GIGAMINUTE = 60000000000
    KILOHOUR = 3600000
    MEGAHOUR = 3600000000
    GREAT_YEAR = 813285766944
    
# Default units for timespot representation
DEFAULT_TIMESPOT_UNIT_SET = [TimespotUnit.YEAR, TimespotUnit.DAY, TimespotUnit.HOUR, TimespotUnit.MINUTE, TimespotUnit.SECOND]

class Timespot:
    """A specific point in time within a timeline.
    Attributes:
        timestamp (float): The timestamp of the timespot, measured in seconds.
        timeline (Timeline): The timeline this timespot belongs to.
    """
    def __init__(self, timestamp: float, timeline: Timeline | None = None) -> None:
        """
        :param self: Description
        :param timestamp: Description
        :type timestamp: float
        :param timeline: Description
        :type timeline: Timeline | None
        """
        Timeline.ensure_default_timeline_exists()
        self.timestamp: float = timestamp
        self.timeline: Timeline | None = timeline if timeline is not None else Timeline.DEFAULT_REGISTRY.get_timeline(0) \
            if Timeline.DEFAULT_REGISTRY is not None else None  # unnecesary check, but pylance complains otherwise
        
    def __repr__(self) -> str:
        return f"<Timespot>(T+{round(self.timestamp, 0)}s, timeline={self.timeline.name!r})" \
            if self.timeline is not None else f"<Timespot>(T+{round(self.timestamp, 0)}s, timeline=None)"
    
    def __str__(self) -> str:
        return f"TS({round(self.timestamp, 2)}s on {self.timeline.name})" \
            if self.timeline is not None else f"TS({round(self.timestamp, 2)}s on None)"
    
    def __eq__(self, other) -> bool:
        return (self.timestamp == other.timestamp and self.timeline == other.timeline) if isinstance(other, Timespot) else False
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Timespot):
            return NotImplemented
        if self.timeline != other.timeline:
            raise ValueError("Cannot compare Timespots from different Timelines.")
        return self.timestamp < other.timestamp
    
    def __le__(self, other) -> bool:    
        if not isinstance(other, Timespot):
            return NotImplemented
        if self.timeline != other.timeline:
            raise ValueError("Cannot compare Timespots from different Timelines.")
        return self.timestamp <= other.timestamp
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Timespot):
            return NotImplemented
        if self.timeline != other.timeline:
            raise ValueError("Cannot compare Timespots from different Timelines.")
        return self.timestamp > other.timestamp
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, Timespot):
            return NotImplemented
        if self.timeline != other.timeline:
            raise ValueError("Cannot compare Timespots from different Timelines.")
        return self.timestamp >= other.timestamp
    
    def __sub__(self, other) -> 'Timespot':
        if isinstance(other, float):
            self.timestamp -= other
            return self
        elif isinstance(other, int):
            self.timestamp -= float(other)
            return self
        else:
            return NotImplemented
        
    def __add__(self, other) -> 'Timespot':
        if isinstance(other, float):
            self.timestamp += other
            return self
        elif isinstance(other, int):
            self.timestamp += float(other)
            return self
        else:
            return NotImplemented
        
    def copy(self) -> 'Timespot':
        """Creates a copy of this Timespot.
        
        :return: A new Timespot instance with the same timestamp and timeline.
        :rtype: Timespot
        """
        return Timespot(self.timestamp, self.timeline)
    
    # Properties
    @property
    def minutes(self) -> float:
        """Returns the timestamp in minutes."""
        return self.timestamp / 60.0
    @property
    def hours(self) -> float:
        """Returns the timestamp in hours."""
        return self.timestamp / 3600.0
    @property
    def days(self) -> float:
        """Returns the timestamp in days."""
        return self.timestamp / 86400.0
    @property
    def weeks(self) -> float:
        """Returns the timestamp in weeks."""
        return self.timestamp / 604800.0
    @property
    def years(self) -> float:   
        """Returns the timestamp in classical gregorian earth years."""
        return self.timestamp / 31556952
    @property
    def julian_years(self) -> float:
        """Returns the timestamp in Julian years."""
        return self.timestamp / 31557600
    
    # Methods to represent values in different units
    def to_unit(self, unit: TimespotUnit) -> float:
        """Converts the timestamp to the specified unit.
        
        :param unit: The unit to convert to.
        :type unit: TimespotUnit
        :return: The timestamp in the specified unit.
        :rtype: float
        """
        return self.timestamp / unit.value
    
    def to_unit_set(self, unit_set: list[TimespotUnit] = DEFAULT_TIMESPOT_UNIT_SET) -> dict:
        """Converts the timestamp to a set of specified units.
        
        :param unit_set: The set of units to convert to.
        :type unit_set: list[TimespotUnit]
        :return: A dictionary with the units as keys and the converted values as values.
        :rtype: dict
        """
        # Sort units in descending order of their value to make conversion meaningful
        unit_set = sorted(unit_set, key=lambda u: u.value, reverse=True)

        # Create dictionary to hold results in pairs of unit: value
        # all units except the smallest will be floored to get meaningful representation
        result = {}
        remaining_time = self.timestamp
        for unit in unit_set:
            if unit == unit_set[-1]:  # smallest unit, keep the remainder as is
                result[unit] = remaining_time / unit.value
                break # exit the loop
            result[unit] = remaining_time // unit.value
            remaining_time %= unit.value

        return result
    
