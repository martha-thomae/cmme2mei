from xml.etree.ElementTree import Element

from model.events import Event
from model.proportion import Proportion


class ProportionEvent(Event):
    """
    Represents an event containing a Proportion (numerator and denominator).
    """
    def __init__(self, proportion: Proportion):
        self.proportion = proportion

    @classmethod
    def parse(cls, element: Element) -> 'ProportionEvent':
        """
        Parses a ProportionEvent from an XML element.

        Args:
            element: The XML element containing ProportionEvent data.

        Returns:
            A ProportionEvent object.
        """
        proportion = Proportion.parse(element)
        return cls(proportion)

    def __eq__(self, other):
        if isinstance(other, ProportionEvent):
            return self.proportion == other.proportion
        return False

    def __repr__(self):
        return f"ProportionEvent(Proportion={self.proportion})"
