from timeline import Timeline
from timespot import Timespot

class Timerange:
    def __init__(self, start: Timespot, end: Timespot) -> None:
        """
        Docstring for __init__
        
        :param self: Description
        :param start: Description
        :type start: Timespot
        :param end: Description
        :type end: Timespot
        """
        if start.timeline != end.timeline:
            raise ValueError("Start and end Timespots must belong to the same Timeline.")
        if start.timestamp < end.timestamp:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start
        
        self.timeline = start.timeline

    @property
    def duration(self) -> float:
        """Returns the duration of the Timerange in seconds."""
        return self.end.timestamp - self.start.timestamp