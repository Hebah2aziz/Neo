class NEODatabase:
    """A database of Near-Earth Objects (NEOs) and their close approaches.

    This class links NEOs with their corresponding close approaches
    and allows retrieval and filtered queries based on designation, name, or approach criteria.
    """

    def __init__(self, neos, approaches):
        """Initialize the database with collections of NEOs and close approaches.

        Args:
            neos (iterable): A collection of NearEarthObject instances.
            approaches (iterable): A collection of CloseApproach instances.
        """
        self._neos = neos
        self._approaches = approaches

        # Internal mappings for quick lookups
        self._neos_by_designation = {neo.designation: neo for neo in neos}
        self._neos_by_name = {neo.name: neo for neo in neos if neo.name}

        # Link each close approach to its corresponding NEO
        for approach in self._approaches:
            neo = self._neos_by_designation.get(approach.designation)
            approach.neo = neo
            if neo:
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Find and return a NEO by its primary designation.

        Args:
            designation (str): The designation of the NEO.

        Returns:
            NearEarthObject or None: The matching NEO, or None if not found.
        """
        return self._neos_by_designation.get(designation)

    def get_neo_by_name(self, name):
        """Find and return a NEO by its name.

        Args:
            name (str): The name of the NEO.

        Returns:
            NearEarthObject or None: The matching NEO, or None if not found.
        """
        return self._neos_by_name.get(name)

    def query(self, filters=()):
        """Query close approaches to find those matching all specified filters.

        Args:
            filters (iterable): A collection of filter callables.

        Yields:
            CloseApproach: Approaches that match all given filters.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach
