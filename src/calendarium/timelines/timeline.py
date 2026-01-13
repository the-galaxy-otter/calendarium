class Timeline:
    """Class representing a timeline.
    Note that timelines are usually managed by TimelineRegistry objects. Use them as factory objects.

    attributes:
        name (str): The name of the timeline.
        index (int): The index of the timeline in the registry.
        hash (int): The hash of the timeline.
        registry (TimelineRegistry | None): The registry this timeline belongs to.
        derived_from (Timeline | None): The timeline this timeline is derived from.
        scale_factor (float): The scale factor relative to the parent timeline.
        displaysment (float): The basic displacement relative to the parent timeline.
        skips_list (list): A list of skips relative to the parent timeline.
    """

    DEFAULT_REGISTRY: TimelineRegistry | None = None
    
    def __init__(self, name: str | None = None, *args, \
                scale_factor = 1.0, \
                displaysment=0.0, skips_list:list | None = None, \
                registry: TimelineRegistry | None = None) -> None:
        # registry preparation
        if registry is None and Timeline.DEFAULT_REGISTRY is not None:
            registry = Timeline.DEFAULT_REGISTRY
        elif registry is None:
            Timeline.ensure_default_registry_exists() # installs fresh registry to class attribute if needed, but pylance doesn't understand it
            registry = Timeline.DEFAULT_REGISTRY
        
        # Default attributes assignment
        self.name = name if name is not None else f"Unnamed timeline"
        self.index, self.hash = -1, -1 # -1 symbolizes timeline is unregistered, will be changed on registration
        self.registry: TimelineRegistry | None = None

        # Timeline derivation attributes assignment
        self.derived_from: Timeline | None = None
        self.scale_factor: float = scale_factor
        self.displaysment: float = displaysment
        self.skips_list: list = skips_list if skips_list is not None else []

        # Register this instance
        if registry is not None:
            registry.register_timeline(self)
    
    
    def __repr__(self) -> str:
        return f"<Timeline>({self.name!r}, index={self.index})"

    def __str__(self) -> str:
        return f"T({self.name})"
    
    def __hash__(self) -> int:
        return self.hash
    
    def __eq__(self, other) -> bool:
        return self.hash == other.hash if isinstance(other, Timeline) else False
    
    # Properties
    @property
    def is_default(self) -> bool:
        """Whether this timeline is the default timeline."""
        return self.index == 0
    
    @property
    def is_derived(self) -> bool:
        """Whether this timeline is derived from another timeline."""
        return self.derived_from is not None
    
    # Alternative ways of creating instancees
    def derive_new_timeline(self, \
                            name: str | None = None, \
                            scale_factor: float = 1.0, \
                            displaysment: float = 0.0, \
                            skips_list: list | None = None) -> 'Timeline':
        """Derives a new timeline from this timeline.
        Args:
            name (str): The name of the new timeline.
            scale_factor (float): The scale factor relative to this timeline.
            displaysment (float): The basic displacement relative to this timeline.
            skips_list (list | None): A list of skips relative to this timeline."""
        new_timeline = Timeline(
            name = name if name is not None else f"{self.name} (derived)",
            scale_factor = scale_factor,
            displaysment = displaysment,
            skips_list = skips_list
        )
        new_timeline.derived_from = self
        return new_timeline

    # Tool functions:
    @classmethod
    def ensure_default_timeline_exists(cls) -> None:
        """Ensures that the default timeline exists."""
        Timeline.ensure_default_registry_exists()
        if Timeline.DEFAULT_REGISTRY is not None and 0 not in Timeline.DEFAULT_REGISTRY.instantiated_sets:
            Timeline(name="Default Timeline")
    
    @classmethod
    def ensure_default_registry_exists(cls) -> None:
        """Ensures that the default timeline registry exists."""
        if cls.DEFAULT_REGISTRY is None:
            cls.DEFAULT_REGISTRY = TimelineRegistry()


class TimelineRegistry:
    """Factory class for managing Timeline instances.
    attributes:
        instantiated_sets (dict): A dictionary of all instantiated timelines.
        instantiated_count (int): The number of instantiated timelines.
    """
    def __init__(self) -> None:
        self.instantiated_sets: dict[int, Timeline] = {}
        self.instantiated_count = 0
    
    def __getitem__(self, index: int) -> Timeline | None:
        return self.get_timeline(index)
    
    def get_timeline(self, index: int) -> Timeline | None:
        """Retrieves a timeline by its index.
        Args:
            index (int): The index of the timeline to retrieve.
        Returns:
            Timeline | None: The timeline with the specified index, or None if not found."""
        return self.instantiated_sets.get(index, None)
    
    def get_new_index(self) -> int:
        """Gets a new unique index for a timeline.
        Returns:
            int: A new unique index."""
        result = self.instantiated_count
        self.instantiated_count += 1
        return result
    
    def register_timeline(self, timeline: Timeline) -> None:
        """Registers a new timeline.
        Args:
            timeline (Timeline): The timeline to register."""
        timeline.index = self.get_new_index() # updates registry counter automatically
        timeline.hash = hash(f"{timeline.name}-{timeline.index}")
        timeline.registry = self
        self.instantiated_sets[timeline.index] = timeline
    
    def unregister_timeline(self, timeline: Timeline) -> None:
        """Unregisters a timeline.
        Args:
            timeline (Timeline): The timeline to unregister."""
        if timeline.index in self.instantiated_sets:
            del self.instantiated_sets[timeline.index]
            timeline.index = -1
            timeline.hash = -1
            timeline.registry = None

    def clear_registry(self) -> None:
        """Clears the registry of all timelines."""
        for timeline in self.instantiated_sets.values():
            timeline.index = -1
            timeline.hash = -1
            timeline.registry = None
        self.instantiated_sets.clear()
        self.instantiated_count = 0
    
    def create_and_register_new_timeline(self, \
                        name: str | None = None, \
                        scale_factor: float = 1.0, \
                        displaysment: float = 0.0, \
                        skips_list: list | None = None) -> Timeline:
        """Creates and registers a new timeline. Expectable, isn't it?
        Args:
            name (str | None): The name of the new timeline.
            scale_factor (float): The scale factor relative to the parent timeline.
            displaysment (float): The basic displacement relative to the parent timeline.
            skips_list (list | None): A list of skips relative to the parent timeline.
        """
        new_timeline = Timeline(
            name = name,
            scale_factor = scale_factor,
            displaysment = displaysment,
            skips_list = skips_list,
            registry = self
        )
        return new_timeline