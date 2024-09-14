from typing import List, Optional
from xml.etree.ElementTree import Element

class ModernText:
    """
    Represents modern text elements like syllables for a note, with optional word endings.
    """
    def __init__(self, syllables: List[Optional[str]], has_word_end: bool):
        self.syllables = syllables
        self.has_word_end = has_word_end

    @classmethod
    def parse(cls, element: Optional[Element]) -> Optional['ModernText']:
        """
        Parses ModernText from an XML element.

        Args:
            element: The XML element containing ModernText data.

        Returns:
            A ModernText object, or None if the element is None.
        """
        if element is None:
            return None

        syllables = []
        has_word_end = False

        # Parse Syllable elements
        for syllable_el in element.findall('{http://www.cmme.org}Syllable'):
            syllables.append(syllable_el.text)

        # Check if WordEnd is present
        word_end_el = element.find('{http://www.cmme.org}WordEnd')
        if word_end_el is not None:
            has_word_end = True

        return cls(syllables, has_word_end)

    def __eq__(self, other):
        if isinstance(other, ModernText):
            return self.syllables == other.syllables and self.has_word_end == other.has_word_end
        return False

    def __repr__(self):
        return f"ModernText(Syllables={self.syllables}, HasWordEnd={self.has_word_end})"


