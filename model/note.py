from typing import Optional
from xml.etree.ElementTree import Element

from model.pitch import Pitch
from model.modern_text import ModernText


class NoteEvent:
    """
    Represents a musical note event, including type, pitch, ligature, stem direction, and modern text.
    """
    def __init__(self, note_type: Optional[str], pitch: Optional[Pitch], lig: Optional[str],
                 stem_dir: Optional[str], stem_side: Optional[str], modern_text: Optional[ModernText]):
        self.note_type = note_type
        self.pitch = pitch
        self.lig = lig
        self.stem_dir = stem_dir
        self.stem_side = stem_side
        self.modern_text = modern_text

    @classmethod
    def parse(cls, element: Element) -> 'NoteEvent':
        """
        Parses a NoteEvent from an XML element.

        Args:
            element: The XML element containing NoteEvent data.

        Returns:
            A NoteEvent object.
        """
        # Parse note type
        note_type = element.find('{http://www.cmme.org}Type').text if element.find('{http://www.cmme.org}Type') is not None else None

        pitch = Pitch.parse(element) # the elements of the pitch are contained in the Note

        # Parse Ligature (Lig)
        lig = element.find('{http://www.cmme.org}Lig').text if element.find('{http://www.cmme.org}Lig') is not None else None

        # Parse Stem direction & stem sides (optional)
        stem_dir = element.find('{http://www.cmme.org}Stem/{http://www.cmme.org}Dir').text if element.find('{http://www.cmme.org}Stem/{http://www.cmme.org}Dir') is not None else None
        stem_side = element.find('{http://www.cmme.org}Stem/{http://www.cmme.org}Side').text if element.find('{http://www.cmme.org}Stem/{http://www.cmme.org}Side') is not None else None

        # Parse ModernText (optional)
        modern_text_element = element.find('{http://www.cmme.org}ModernText')
        modern_text = ModernText.parse(modern_text_element) if modern_text_element is not None else None

        return cls(note_type, pitch, lig, stem_dir, stem_side, modern_text)

    def __eq__(self, other):
        if isinstance(other, NoteEvent):
            return (self.note_type == other.note_type and
                    self.pitch == other.pitch and
                    self.lig == other.lig and
                    self.stem_dir == other.stem_dir and
                    self.stem_side == other.stem_side and
                    self.modern_text == other.modern_text)
        return False

    def __repr__(self):
        return (f"NoteEvent(NoteType={self.note_type}, Pitch={self.pitch}, Lig={self.lig}, "
                f"StemDir={self.stem_dir}, StemSide={self.stem_side}, ModernText={self.modern_text})")
