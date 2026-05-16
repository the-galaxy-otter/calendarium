from calendarium.timelines.TimelineRepresentationUnits import TimelineRepresentationUnits

class TimelineRepresentor:
    """Class represence a n ordered sequence of units. Provides methods to convert secons  into a sequence of values in the specified units.
    The units are stored in a tuple in descending order of values.
    
    Attributes:
        units (tuple): A tuple of TimelineRepresentationUnits in descending order of values.
    
    Methods:
        FilterUnits(*args: TimelineRepresentationUnits) -> tuple: A static method that filters the input units to remove duplicates.
            The filtered units are returned as a tuple in descending order of values.
        
        seconds_to_dict(seconds: int) -> dict: Converts the input seconds into a sequence of values in the specified units.

        dict_to_seconds(unit_counts: dict) -> int: Converts a dictionary of unit counts back into seconds.
    """
    
    @staticmethod
    def FilterUnits(*args: TimelineRepresentationUnits):
        filtered_units = []
        filter_names = []

        for arg in args:
            if arg == TimelineRepresentationUnits.Second or arg.name in filter_names:
                continue
            else:
                filter_names.append(arg.name)
                filtered_units.append(arg)
        # filter the list to appear in descending order of values and convert into immutable tuple of unique values
        return tuple(sorted(filtered_units, key=lambda x: x.value, reverse=True))
    
    def __init__(self, *args: TimelineRepresentationUnits) -> None:
        if len(args) >= 1:
            self.units = TimelineRepresentor.FilterUnits(*args)
        else:
            # Guarantees it has seconds as a final unit at least
            self.units = (TimelineRepresentationUnits.Second,)

    def __repr__(self) -> str:
        return f"TimelineRepresentor(units={self.units})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def seconds_to_dict(self, seconds: int) -> dict[TimelineRepresentationUnits, int]:
        """Converts the input seconds into a sequence of values in the specified units.
        
        :param seconds: The number of seconds to convert.
        :type seconds: int
        
        :rtype: dict[TimelineRepresentationUnits, int]
        :returns: A dictionary where the keys are the units and the values are the counts of each unit in the input seconds.
        """
        result = {}
        remaining_seconds = seconds

        for unit in self.units:
            unit_value = unit.value
            unit_count = remaining_seconds // unit_value
            result[unit] = unit_count
            remaining_seconds -= unit_count * unit_value
        
        return result
    
    def dict_to_seconds(self, unit_counts: dict[TimelineRepresentationUnits, int]) -> int:
        """Converts a dictionary of unit counts back into seconds.
        
        :param unit_counts: A dictionary where the keys are the units and the values are the counts of each unit.
        :type unit_counts: dict[TimelineRepresentationUnits, int]
        
        :rtype: int
        :returns: The total number of seconds represented by the input unit counts.
        """
        total_seconds: int = 0

        for unit, count in unit_counts.items():
            total_seconds += int(unit.value * count)
        
        return total_seconds
    
    def seconds_to_tuple(self, seconds) -> tuple[int]:
        """Converts the input seconds into a sequence of values in the specified units.
        
        :param seconds: The number of seconds to convert.
        :type seconds: int
        
        :returns: An ordered tuple of values in propper descending order
        :rtype: tuple[int]
        """
        result = []
        remaining_seconds = seconds

        for unit in self.units:
            unit_value = unit.value
            unit_count = remaining_seconds // unit_value
            result.append(unit_count)
            remaining_seconds -= unit_count * unit_value
        
        return tuple(result)
        
    
# Non-class members
DEFAULT_UNIT_SET = TimelineRepresentor(TimelineRepresentationUnits.Second,
                                       TimelineRepresentationUnits.Minute,
                                       TimelineRepresentationUnits.Hour,
                                       TimelineRepresentationUnits.Day,
                                       TimelineRepresentationUnits.Year)
        