from typing import Optional
from xml.etree.ElementTree import Element


class Pitch:
    """
    Represents a musical pitch with a letter name and octave number.
    """

    def __init__(self, letter_name: Optional[str], octave_num: Optional[int]):
        self.letter_name = letter_name
        self.octave_num = octave_num

    def __repr__(self):
        return f"Pitch(LetterName={self.letter_name}, OctaveNum={self.octave_num})"

    def __eq__(self, other):
        if not isinstance(other, Pitch):
            return False
        return self.letter_name == other.letter_name and self.octave_num == other.octave_num

    @classmethod
    def parse(cls, element: Element) -> 'Pitch':
        if element is None:
            return None
        letter_name = element.find('{http://www.cmme.org}LetterName').text if element.find('{http://www.cmme.org}LetterName') is not None else None
        octave_num = int(element.find('{http://www.cmme.org}OctaveNum').text) if element.find('{http://www.cmme.org}OctaveNum') is not None else None
        return cls(letter_name, octave_num)
