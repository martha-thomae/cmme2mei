from typing import Optional
from xml.etree.ElementTree import Element


class OriginalTextEvent:
    """
    Represents an original text event, containing a phrase from the original text.
    """
    def __init__(self, phrase: Optional[str]):
        self.phrase = phrase

    @classmethod
    def parse(cls, element: Element) -> 'OriginalTextEvent':
        """
        Parses an OriginalTextEvent from an XML element.

        Args:
            element: The XML element containing OriginalTextEvent data.

        Returns:
            An OriginalTextEvent object.
        """
        phrase = element.find('{http://www.cmme.org}Phrase').text if element.find('{http://www.cmme.org}Phrase') is not None else None
        return cls(phrase)

    def __eq__(self, other):
        if isinstance(other, OriginalTextEvent):
            return self.phrase == other.phrase
        return False

    def __repr__(self):
        return f"OriginalTextEvent(Phrase={self.phrase})"
