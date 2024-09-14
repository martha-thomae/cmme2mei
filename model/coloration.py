from typing import Optional
from xml.etree.ElementTree import Element

from model.events import Event


class ColorAndFillData:
    def __init__(self, color: Optional[str] = None, fill: Optional[str] = None):
        self.color = color
        self.fill = fill

    @classmethod
    def parse(cls, element: Element) -> Optional['ColorAndFillData']:
        if element is None:
            return None

        color_el = element.find('{http://www.cmme.org}Color')
        fill_el = element.find('{http://www.cmme.org}Fill')

        color = color_el.text if color_el is not None else None
        fill = fill_el.text if fill_el is not None else None

        return cls(color, fill)


class ColorationData:
    def __init__(self, primary_color: ColorAndFillData, secondary_color: Optional[ColorAndFillData] = None):
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    @classmethod
    def parse(cls, element: Element) -> Optional['ColorationData']:
        if element is None:
            return None

        # Parse the primary color (required)
        primary_color_el = element.find('{http://www.cmme.org}PrimaryColor')
        primary_color_data = ColorAndFillData.parse(primary_color_el)

        if primary_color_data is None:
            # Primary color is required, if not found, return None
            return None

        # Parse the secondary color (optional)
        secondary_color_el = element.find('{http://www.cmme.org}SecondaryColor')
        secondary_color_data = ColorAndFillData.parse(secondary_color_el)

        return cls(primary_color_data, secondary_color_data)


class BaseColoration:
    def __init__(self, coloration_data: ColorationData):
        self.coloration_data = coloration_data

    @classmethod
    def parse(cls, element: Element) -> Optional['BaseColoration']:
        if element is None:
            return None

        # Parse the coloration data
        coloration_data = ColorationData.parse(element)

        if coloration_data is None:
            # If there's no valid coloration data, return None
            return None

        return cls(coloration_data)

class ColorChangeEvent(Event):
    """
    Represents a color change event in musical notation, containing primary and secondary colors.
    """
    def __init__(self, primary_color: Optional[str], secondary_color: Optional[str]):
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    @classmethod
    def parse(cls, element: Element) -> 'ColorChangeEvent':
        """
        Parses a ColorChangeEvent from an XML element.

        Args:
            element: The XML element containing ColorChangeEvent data.

        Returns:
            A ColorChangeEvent object.
        """
        primary_color = element.find('{http://www.cmme.org}PrimaryColor').text if element.find('{http://www.cmme.org}PrimaryColor') is not None else None
        secondary_color = element.find('{http://www.cmme.org}SecondaryColor').text if element.find('{http://www.cmme.org}SecondaryColor') is not None else None

        return cls(primary_color, secondary_color)

    def __eq__(self, other):
        if isinstance(other, ColorChangeEvent):
            return self.primary_color == other.primary_color and self.secondary_color == other.secondary_color
        return False

    def __repr__(self):
        return f"ColorChangeEvent(PrimaryColor={self.primary_color}, SecondaryColor={self.secondary_color})"
