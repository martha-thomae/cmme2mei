from abc import ABC
from typing import List, Optional
from xml.etree.ElementTree import Element

from model.coloration import BaseColoration
from model.events import Event


class EventList:
    """
    Represents the events inside a Voice, such as Clef, Note, Rest, or complex structures like VariantReadings or EditorialData.
    """
    def __init__(self, events: List[Event]):
        self.events = events

    @classmethod
    def parse(cls, element: Element) -> 'EventList':
        events = []

        # Parse all standard events and other structures in EventListData
        for event_el in element:
            if event_el.tag.endswith('VariantReadings'):
                from model.reading import VariantReadings
                variant_reading = VariantReadings.parse(event_el)
                events.append(variant_reading)
            elif event_el.tag.endswith('EditorialData'):
                from model.reading import EditorialData
                editorial_data = EditorialData.parse(event_el)
                events.append(editorial_data)
            else:
                # For standard events handled by SingleOrMultiEventData
                from model.event_factory import EventFactory
                event = EventFactory.create(event_el)
                events.append(event)

        return EventList(events)


class Voice:
    """
    Represents a voice in the MensuralMusic, Plainchant, or TextSection.
    Each voice has a VoiceNum, an optional list of MissingVersionID, and an EventList.
    """

    def __init__(self, voice_num: int, missing_version_ids: Optional[List[str]], event_list: EventList):
        self.voice_num = voice_num
        self.missing_version_ids = missing_version_ids if missing_version_ids is not None else []
        self.event_list = event_list

    @classmethod
    def parse(cls, element: Element) -> 'Voice':
        # Parse the VoiceNum (required)
        voice_num_el = element.find('{http://www.cmme.org}VoiceNum')
        voice_num = int(voice_num_el.text) if voice_num_el is not None else None

        # Parse MissingVersionID (optional, can occur multiple times)
        missing_version_ids = [mv_el.text for mv_el in element.findall('{http://www.cmme.org}MissingVersionID')]

        # Parse EventList (required)
        event_list_el = element.find('{http://www.cmme.org}EventList')
        event_list = EventList.parse(event_list_el) if event_list_el is not None else None

        return Voice(voice_num, missing_version_ids, event_list)


class TacetData:
    """
    Represents the TacetData group, which contains VoiceNum and TacetText elements.
    """
    def __init__(self, voice_num: int, tacet_text: str):
        self.voice_num = voice_num
        self.tacet_text = tacet_text

    @classmethod
    def parse(cls, element: Element) -> 'TacetData':
        # Parse the VoiceNum element (unsigned integer)
        voice_num_el = element.find('{http://www.cmme.org}VoiceNum')
        voice_num = int(voice_num_el.text) if voice_num_el is not None else None

        # Parse the TacetText element (string)
        tacet_text_el = element.find('{http://www.cmme.org}TacetText')
        tacet_text = tacet_text_el.text if tacet_text_el is not None else None

        # Return a TacetData object
        return cls(voice_num, tacet_text)


class AbstractMusicSectionContent(ABC):
    def __init__(self, section_type: str, num_voices: int, voices: List[Voice]):
        self.section_type = section_type
        self.num_voices = num_voices
        self.voices = voices

    """
        Used for plainchant and mensural notation
    """
    @classmethod
    def parse(cls, element: Element):
        # Parse NumVoices (required)
        num_voices_el = element.find('{http://www.cmme.org}NumVoices')
        num_voices = int(num_voices_el.text) if num_voices_el is not None else 0

        # Parse BaseColoration (optional)
        base_coloration_el = element.find('{http://www.cmme.org}BaseColoration')
        base_coloration = BaseColoration.parse(base_coloration_el) if base_coloration_el is not None else None

        # Parse TacetInstruction elements (optional, can occur multiple times)
        tacet_instructions = []
        tacet_instruction_els = element.findall('{http://www.cmme.org}TacetInstruction')
        for tacet_instruction_el in tacet_instruction_els:
            tacet_instructions.append(TacetData.parse(tacet_instruction_el))

        # Parse Voice elements (must occur at least once)
        voices = [Voice.parse(voice_el) for voice_el in element.findall('{http://www.cmme.org}Voice')]

        # Return all common data
        return num_voices, base_coloration, tacet_instructions, voices


class MensuralMusic(AbstractMusicSectionContent):
    def __init__(self, num_voices: int, base_coloration: Optional[BaseColoration],
                 tacet_instructions: Optional[List[TacetData]], voices: List[Voice]):
        super().__init__('MensuralMusic', num_voices, voices)
        self.base_coloration = base_coloration
        self.tacet_instructions = tacet_instructions if tacet_instructions is not None else []

    @classmethod
    def parse(cls, element: Element) -> 'MensuralMusic':
        num_voices, base_coloration, tacet_instructions, voices = AbstractMusicSectionContent.parse(element)
        return cls(num_voices, base_coloration, tacet_instructions, voices)


class Plainchant(AbstractMusicSectionContent):
    def __init__(self, num_voices: int, base_coloration: Optional[BaseColoration],
                 tacet_instructions: Optional[List[TacetData]], voices: List[Voice]):
        super().__init__('Plainchant', num_voices, voices)
        self.base_coloration = base_coloration
        self.tacet_instructions = tacet_instructions if tacet_instructions is not None else []

    @classmethod
    def parse(cls, element: Element) -> 'Plainchant':
        num_voices, base_coloration, tacet_instructions, voices = AbstractMusicSectionContent.parse(element)
        return cls(num_voices, base_coloration, tacet_instructions, voices)


class TextSection(AbstractMusicSectionContent):
    def __init__(self, num_voices: int, voices: List[Voice]):
        super().__init__('Text', num_voices, voices)

    @classmethod
    def parse(cls, element: Element) -> 'TextSection':
        # Parse the Content element
        content_elements = element.findall('{http://www.cmme.org}Content')
        contents = [content_el.text for content_el in content_elements if content_el.text is not None]

        # Return the TextSection object with the parsed contents
        return cls(contents)

class MusicSection:
    def __init__(self, content: AbstractMusicSectionContent):
        self.content = content

    @classmethod
    def parse(cls, element: Element) -> 'MusicSection':
        # Try to find the MensuralMusic element
        mensural_music_el = element.find('{http://www.cmme.org}MensuralMusic')
        if mensural_music_el is not None:
            content = MensuralMusic.parse(mensural_music_el)
            return MusicSection(content)

        # Try to find the Plainchant element
        plainchant_el = element.find('{http://www.cmme.org}Plainchant')
        if plainchant_el is not None:
            content = Plainchant.parse(plainchant_el)
            return MusicSection(content)

        # Try to find the Text element
        text_el = element.find('{http://www.cmme.org}Text')
        if text_el is not None:
            content = TextSection.parse(text_el)
            return MusicSection(content)

        # If no known content type is found, raise an error
        raise ValueError("Unsupported section type in MusicSection")

