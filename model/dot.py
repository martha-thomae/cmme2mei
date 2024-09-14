from typing import Optional
from xml.etree.ElementTree import Element

from model.pitch import Pitch


class DotEvent:
    """
    Represents a dot event in musical notation, which may include a pitch.
    """
    def __init__(self, pitch: Optional[Pitch]):
        self.pitch = pitch

    @classmethod
    def parse(cls, element: Element) -> 'DotEvent':
        """
        Parses a DotEvent from an XML element.

        Args:
            element: The XML element containing DotEvent data.
            parse_pitch: Helper function to parse Pitch.

        Returns:
            A DotEvent object.
        """
        pitch_element = element.find('{http://www.cmme.org}Pitch')
        pitch = Pitch.parse(pitch_element) if pitch_element is not None else None

        return cls(pitch)

    def __eq__(self, other):
        if isinstance(other, DotEvent):
            return self.pitch == other.pitch
        return False

    def __repr__(self):
        return f"DotEvent(Pitch={self.pitch})"
