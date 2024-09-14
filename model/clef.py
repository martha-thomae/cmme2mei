from typing import Optional
from xml.etree.ElementTree import Element

from model.events import EventAttributes, Event
from model.pitch import Pitch


class ClefEvent(Event):
    """
    Represents a clef event in musical notation.
    """
    def __init__(self, appearance: Optional[str], staff_loc: Optional[int], pitch: Optional[Pitch],
                 event_attributes: EventAttributes, signature: bool):
        self.appearance = appearance
        self.staff_loc = staff_loc
        self.pitch = pitch
        self.event_attributes = event_attributes
        self.signature = signature

    @classmethod
    def parse(cls, element: Element) -> 'ClefEvent':
        """
        Parses a ClefEvent from an XML element.

        Args:
            element: The XML element that contains ClefEvent data.
            parse_event_attributes: A helper function to parse event attributes.

        Returns:
            A ClefEvent object.
        """
        # Parse Appearance
        appearance = element.find('{http://www.cmme.org}Appearance').text if element.find('{http://www.cmme.org}Appearance') is not None else None

        # Parse StaffLoc as an integer
        staff_loc = int(element.find('{http://www.cmme.org}StaffLoc').text) if element.find('{http://www.cmme.org}StaffLoc') is not None else None

        # Parse Pitch (which uses the Locus group)
        pitch_element = element.find('{http://www.cmme.org}Pitch')
        if pitch_element is not None:
            letter_name = pitch_element.find('{http://www.cmme.org}LetterName').text if pitch_element.find('{http://www.cmme.org}LetterName') is not None else None
            octave_num = int(pitch_element.find('{http://www.cmme.org}OctaveNum').text) if pitch_element.find('{http://www.cmme.org}OctaveNum') is not None else None
            pitch = Pitch(letter_name, octave_num)
        else:
            pitch = None

        # Parse Signature (optional)
        signature = element.find('{http://www.cmme.org}Signature') is not None

        # Parse EventAttributes (referenced group)
        event_attributes = EventAttributes.parse(element)

        return cls(appearance, staff_loc, pitch, event_attributes, signature)

    def __eq__(self, other):
        if not isinstance(other, ClefEvent):
            return False
        return (self.appearance == other.appearance and
                self.staff_loc == other.staff_loc and
                self.pitch == other.pitch and
                self.event_attributes == other.event_attributes and
                self.signature == other.signature)


    def __repr__(self):
        return (f"ClefEvent(Appearance={self.appearance}, StaffLoc={self.staff_loc}, Pitch={self.pitch}, "
                f"EventAttributes={self.event_attributes}, Signature={self.signature})")
