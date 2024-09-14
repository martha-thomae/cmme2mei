from typing import Optional, Dict
from xml.etree.ElementTree import Element

from model.events import EventAttributes
from model.proportion import Proportion


class MensurationEvent:
    """
    Represents a mensuration event in musical notation.
    """
    def __init__(self, main_symbol: Optional[str], strokes: Optional[int], orientation: Optional[str],
                 dot: bool, number: Optional[Proportion], staff_loc: Optional[int],
                 mens_info: Dict[str, Optional[str]], no_score_effect: bool, event_attributes: EventAttributes):
        self.main_symbol = main_symbol
        self.orientation = orientation
        self.strokes = strokes
        self.dot = dot
        self.number = number
        self.staff_loc = staff_loc
        self.mens_info = mens_info
        self.no_score_effect = no_score_effect
        self.event_attributes = event_attributes

    @classmethod
    def parse(cls, element: Element) -> 'MensurationEvent':
        """
        Parses a MensurationEvent from an XML element.

        Args:
            element: The XML element that contains MensurationEvent data.
            parse_event_attributes: Helper function to parse event attributes.
            parse_proportion: Helper function to parse proportion.

        Returns:
            A MensurationEvent object.
        """
        main_symbol = None
        orientation = None
        strokes = None
        dot = False
        number = None

        # Handle Sign element
        sign_el = element.find('{http://www.cmme.org}Sign')
        if sign_el is not None:
            main_symbol_el = sign_el.find('{http://www.cmme.org}MainSymbol')
            main_symbol = main_symbol_el.text if main_symbol_el is not None else None

            orientation_el = sign_el.find('{http://www.cmme.org}Orientation')
            orientation = orientation_el.text if orientation_el is not None else None

            strokes_el = sign_el.find('{http://www.cmme.org}Strokes')
            strokes = int(strokes_el.text) if strokes_el is not None else None

            dot = sign_el.find('{http://www.cmme.org}Dot') is not None

        # Handle Number element (Proportion group)
        number_el = element.find('{http://www.cmme.org}Number')
        if number_el is not None:
            number = Proportion.parse(number_el)

        # Parse optional StaffLoc
        staff_loc_el = element.find('{http://www.cmme.org}StaffLoc')
        staff_loc = int(staff_loc_el.text) if staff_loc_el is not None else None

        # Parse MensInfo (if present)
        mens_info = {}
        mens_info_el = element.find('{http://www.cmme.org}MensInfo')
        if mens_info_el is not None:
            mens_info['prolatio'] = mens_info_el.find('{http://www.cmme.org}Prolatio').text if mens_info_el.find('{http://www.cmme.org}Prolatio') is not None else None
            mens_info['tempus'] = mens_info_el.find('{http://www.cmme.org}Tempus').text if mens_info_el.find('{http://www.cmme.org}Tempus') is not None else None
            mens_info['modus_minor'] = mens_info_el.find('{http://www.cmme.org}ModusMinor').text if mens_info_el.find('{http://www.cmme.org}ModusMinor') is not None else None
            mens_info['modus_maior'] = mens_info_el.find('{http://www.cmme.org}ModusMaior').text if mens_info_el.find('{http://www.cmme.org}ModusMaior') is not None else None

            tempo_change_el = mens_info_el.find('{http://www.cmme.org}TempoChange')
            if tempo_change_el is not None:
                mens_info['tempo_change'] = Proportion.parse(tempo_change_el)

        # Parse NoScoreEffect (True if present)
        no_score_effect = element.find('{http://www.cmme.org}NoScoreEffect') is not None

        # Parse EventAttributes
        event_attributes = EventAttributes.parse(element)

        # Return the parsed MensurationEvent object
        return cls(main_symbol, strokes, orientation, dot, number, staff_loc, mens_info, no_score_effect, event_attributes)

    def __eq__(self, other):
        if isinstance(other, MensurationEvent):
            return (self.main_symbol == other.main_symbol and
                    self.orientation == other.orientation and
                    self.strokes == other.strokes and
                    self.dot == other.dot and
                    self.number == other.number and
                    self.staff_loc == other.staff_loc and
                    self.mens_info == other.mens_info and
                    self.no_score_effect == other.no_score_effect and
                    self.event_attributes == other.event_attributes)
        return False

    def __repr__(self):
        return (f"MensurationEvent(MainSymbol={self.main_symbol}, Orientation={self.orientation}, Strokes={self.strokes}, "
                f"Dot={self.dot}, Number={self.number}, StaffLoc={self.staff_loc}, MensInfo={self.mens_info}, "
                f"NoScoreEffect={self.no_score_effect}, EventAttributes={self.event_attributes})")
