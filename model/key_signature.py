from typing import Optional
from xml.etree.ElementTree import Element


class ModernKeySignatureEvent:
    """
    Represents a modern key signature event in musical notation, containing an accidental and pitch class.
    """
    def __init__(self, accidental: Optional[str], pitch_class: Optional[str]):
        self.accidental = accidental
        self.pitch_class = pitch_class

    @classmethod
    def parse(cls, element: Element) -> 'ModernKeySignatureEvent':
        """
        Parses a ModernKeySignatureEvent from an XML element.

        Args:
            element: The XML element containing ModernKeySignatureEvent data.

        Returns:
            A ModernKeySignatureEvent object.
        """
        accidental = element.find('{http://www.cmme.org}Accidental').text if element.find('{http://www.cmme.org}Accidental') is not None else None
        pitch_class = element.find('{http://www.cmme.org}PitchClass').text if element.find('{http://www.cmme.org}PitchClass') is not None else None

        return cls(accidental, pitch_class)

    def __eq__(self, other):
        if isinstance(other, ModernKeySignatureEvent):
            return self.accidental == other.accidental and self.pitch_class == other.pitch_class
        return False

    def __repr__(self):
        return f"ModernKeySignatureEvent(Accidental={self.accidental}, PitchClass={self.pitch_class})"
