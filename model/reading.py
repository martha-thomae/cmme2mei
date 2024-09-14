from typing import List, Optional, Dict
from xml.etree.ElementTree import Element

from model.event_factory import EventFactory


class ReadingBase:
    """
    A base class for Reading-related classes that contain common properties such as variant_version_ids, preferred_reading, error, and lacuna.
    """
    def __init__(self, variant_version_ids: List[str], preferred_reading: Optional[str], error: Optional[str],
                 lacuna: bool, music_events: List[Dict]):
        self.variant_version_ids = variant_version_ids
        self.preferred_reading = preferred_reading
        self.error = error
        self.lacuna = lacuna
        self.music_events = music_events

    @classmethod
    def parse_reading(cls, reading_el: Element) -> 'ReadingBase':
        variant_version_ids = [vv_el.text for vv_el in reading_el.findall('{http://www.cmme.org}VariantVersionID')]
        preferred_reading_el = reading_el.find('{http://www.cmme.org}PreferredReading')
        error_el = reading_el.find('{http://www.cmme.org}Error')
        lacuna_el = reading_el.find('{http://www.cmme.org}Lacuna')

        preferred_reading = preferred_reading_el.text if preferred_reading_el is not None else None
        error = error_el.text if error_el is not None else None
        lacuna = lacuna_el is not None

        # Parse Music events
        music_el = reading_el.find('{http://www.cmme.org}Music')
        music_events = []
        if music_el is not None:
            music_events = [EventFactory.create(me_el) for me_el in music_el.findall('{http://www.cmme.org}Event')]

        return cls(variant_version_ids, preferred_reading, error, lacuna, music_events)

    def __eq__(self, other):
        if isinstance(other, ReadingBase):
            return (self.variant_version_ids == other.variant_version_ids and
                    self.preferred_reading == other.preferred_reading and
                    self.error == other.error and
                    self.lacuna == other.lacuna and
                    self.music_events == other.music_events)
        return False

    def __repr__(self):
        return (f"{self.__class__.__name__}(VariantVersionIDs={self.variant_version_ids}, "
                f"PreferredReading={self.preferred_reading}, Error={self.error}, "
                f"Lacuna={self.lacuna}, MusicEvents={self.music_events})")


class Reading(ReadingBase):
    """
    Represents a specific reading with variant version IDs, preferred reading, error, lacuna, and music events.
    Inherits common properties from ReadingBase.
    """
    pass


class VariantReadings:
    """
    Represents a collection of variant readings.
    """
    def __init__(self, readings: List[Reading]):
        self.readings = readings

    @classmethod
    def parse(cls, element: Element) -> 'VariantReadings':
        readings = []
        for reading_el in element.findall('{http://www.cmme.org}Reading'):
            reading = Reading.parse_reading(reading_el)
            readings.append(reading)

        return cls(readings)

    def __eq__(self, other):
        if isinstance(other, VariantReadings):
            return self.readings == other.readings
        return False

    def __repr__(self):
        return f"VariantReadings(Readings={self.readings})"


class OriginalReading(ReadingBase):
    """
    Represents the original reading in editorial data, which can include lacuna and error events.
    Inherits common properties from ReadingBase.
    """
    @classmethod
    def parse(cls, element: Element, parse_single_or_multi_event_data) -> 'OriginalReading':
        return super().parse_reading(element, parse_single_or_multi_event_data)


class EditorialData:
    """
    Represents editorial data, containing new and original readings.
    """
    def __init__(self, new_reading: List[Dict], original_reading: Optional[OriginalReading]):
        self.new_reading = new_reading
        self.original_reading = original_reading

    @classmethod
    def parse(cls, element: Element, parse_single_or_multi_event_data) -> 'EditorialData':
        new_reading_el = element.find('{http://www.cmme.org}NewReading')
        original_reading_el = element.find('{http://www.cmme.org}OriginalReading')

        # Parse new reading events
        new_events = []
        if new_reading_el is not None:
            new_events = [parse_single_or_multi_event_data(ne_el) for ne_el in new_reading_el.findall('{http://www.cmme.org}Event')]

        # Parse original reading events
        original_reading = None
        if original_reading_el is not None:
            original_reading = OriginalReading.parse(original_reading_el, parse_single_or_multi_event_data)

        return cls(new_events, original_reading)

    def __eq__(self, other):
        if isinstance(other, EditorialData):
            return self.new_reading == other.new_reading and self.original_reading == other.original_reading
        return False

    def __repr__(self):
        return f"EditorialData(NewReading={self.new_reading}, OriginalReading={self.original_reading})"
