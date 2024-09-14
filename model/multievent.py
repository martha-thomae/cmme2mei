from typing import List, Optional
from xml.etree.ElementTree import Element

class MultiEvent:
    """
    Represents a collection of multiple events.
    """
    def __init__(self, events: List[Optional[dict]]):
        self.events = events

    @classmethod
    def parse(cls, element: Element) -> 'MultiEvent':
        """
        Parses a MultiEvent from an XML element and returns a MultiEvent instance.

        Args:
            element: The XML element that contains MultiEvent data.
            parse_single_event: A helper function to parse individual event elements.

        Returns:
            A MultiEvent object containing a list of parsed events.
        """
        multi_events = []

        # Iterate over each child element inside MultiEvent and parse it
        for sub_event_el in element:
            from model.event_factory import EventFactory
            event = EventFactory.create(sub_event_el)
            multi_events.append(event)

        return cls(multi_events)

    def __eq__(self, other):
        if isinstance(other, MultiEvent):
            return self.events == other.events
        return False

    def __repr__(self):
        return f"MultiEvent(Events={self.events})"
