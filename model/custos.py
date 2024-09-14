from typing import Optional
from xml.etree.ElementTree import Element
from model.pitch import Pitch


class CustosEvent:
    """
    Represents a custos event in musical notation, which contains a Pitch.
    """
    def __init__(self, pitch: Optional[Pitch]):
        self.pitch = pitch

    @classmethod
    def parse(cls, element: Element) -> 'CustosEvent':
        """
        Parses a CustosEvent from an XML element.

        Args:
            element: The XML element containing CustosEvent data.

        Returns:
            A CustosEvent object.
        """
        pitch = Pitch.parse(element)
        return cls(pitch)

    def __eq__(self, other):
        if isinstance(other, CustosEvent):
            return self.pitch == other.pitch
        return False

    def __repr__(self):
        return f"CustosEvent(Pitch={self.pitch})"
