class Event:
    """
    Base class for all events.
    Each event has a type (e.g., 'Clef', 'Note', 'Dot', etc.).
    """
    def __init__(self, event_type: str):
        self.event_type = event_type

    def __repr__(self):
        return f"{self.__class__.__name__}(Type={self.event_type})"


class EventAttributes:
    def __init__(self, colored: bool = False, ambiguous: bool = False, editorial: bool = False, error: bool = False, editorial_commentary: str = None):
        self.colored = colored
        self.ambiguous = ambiguous
        self.editorial = editorial
        self.error = error
        self.editorial_commentary = editorial_commentary

    def __eq__(self, other):
        if not isinstance(other, EventAttributes):
            return False
        return (self.colored == other.colored and
                self.ambiguous == other.ambiguous and
                self.editorial == other.editorial and
                self.error == other.error and
                self.editorial_commentary == other.editorial_commentary)

    def __repr__(self):
        return (f"EventAttributes(Colored={self.colored}, Ambiguous={self.ambiguous}, "
                f"Editorial={self.editorial}, Error={self.error}, "
                f"EditorialCommentary={self.editorial_commentary})")

    @classmethod
    def parse(cls, element) -> 'EventAttributes':
        """
        Parse the EventAttributes group, which includes optional elements:
        Colored, Ambiguous, Editorial, Error, and EditorialCommentary.
        """
        # Parse Colored (True if present)
        colored = element.find('{http://www.cmme.org}Colored') is not None

        # Parse Ambiguous (True if present)
        ambiguous = element.find('{http://www.cmme.org}Ambiguous') is not None

        # Parse Editorial (True if present)
        editorial = element.find('{http://www.cmme.org}Editorial') is not None

        # Parse Error (True if present)
        error = element.find('{http://www.cmme.org}Error') is not None

        # Parse EditorialCommentary (if present)
        editorial_commentary_element = element.find('{http://www.cmme.org}EditorialCommentary')
        editorial_commentary = editorial_commentary_element.text if editorial_commentary_element is not None else None

        # Create and return EventAttributes object
        return EventAttributes(colored, ambiguous, editorial, error, editorial_commentary)


