from typing import Optional
from xml.etree.ElementTree import Element



class MiscItemEvent:
    """
    Represents a miscellaneous item event, which may include barline data such as the number of lines.
    """
    def __init__(self, num_lines: Optional[str]):
        self.num_lines = num_lines

    @classmethod
    def parse(cls, element: Element) -> Optional['MiscItemEvent']:
        """
        Parses a MiscItemEvent from an XML element.

        Args:
            element: The XML element containing MiscItemEvent data.

        Returns:
            A MiscItemEvent object, or None if no valid data is found.
        """
        barline_el = element.find('{http://www.cmme.org}Barline')
        if barline_el is not None:
            num_lines = barline_el.find('{http://www.cmme.org}NumLines').text if barline_el.find('{http://www.cmme.org}NumLines') is not None else None
            return cls(num_lines)

        return None

    def __eq__(self, other):
        if isinstance(other, MiscItemEvent):
            return self.num_lines == other.num_lines
        return False

    def __repr__(self):
        return f"MiscItemEvent(NumLines={self.num_lines})"
