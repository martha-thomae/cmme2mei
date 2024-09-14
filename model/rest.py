from typing import Optional
from xml.etree.ElementTree import Element

class RestEvent:
    """
    Represents a rest event in musical notation, including type, length, staff line, and spacing information.
    """
    def __init__(self, rest_type: Optional[str], length_num: Optional[str], length_den: Optional[str],
                 bottom_staff_line: Optional[str], num_spaces: Optional[str]):
        self.rest_type = rest_type
        self.length_num = length_num
        self.length_den = length_den
        self.bottom_staff_line = bottom_staff_line
        self.num_spaces = num_spaces

    @classmethod
    def parse(cls, element: Element) -> 'RestEvent':
        """
        Parses a RestEvent from an XML element.

        Args:
            element: The XML element containing RestEvent data.

        Returns:
            A RestEvent object.
        """
        # Parse Rest Type
        rest_type = element.find('{http://www.cmme.org}Type').text if element.find('{http://www.cmme.org}Type') is not None else None

        # Parse Length (Num and Den)
        length_num = element.find('{http://www.cmme.org}Length/Num').text if element.find('{http://www.cmme.org}Length/Num') is not None else None
        length_den = element.find('{http://www.cmme.org}Length/Den').text if element.find('{http://www.cmme.org}Length/Den') is not None else None

        # Parse BottomStaffLine
        bottom_staff_line = element.find('{http://www.cmme.org}BottomStaffLine').text if element.find('{http://www.cmme.org}BottomStaffLine') is not None else None

        # Parse NumSpaces
        num_spaces = element.find('{http://www.cmme.org}NumSpaces').text if element.find('{http://www.cmme.org}NumSpaces') is not None else None

        return cls(rest_type, length_num, length_den, bottom_staff_line, num_spaces)

    def __eq__(self, other):
        if isinstance(other, RestEvent):
            return (self.rest_type == other.rest_type and
                    self.length_num == other.length_num and
                    self.length_den == other.length_den and
                    self.bottom_staff_line == other.bottom_staff_line and
                    self.num_spaces == other.num_spaces)
        return False

    def __repr__(self):
        return (f"RestEvent(RestType={self.rest_type}, LengthNum={self.length_num}, "
                f"LengthDen={self.length_den}, BottomStaffLine={self.bottom_staff_line}, NumSpaces={self.num_spaces})")
