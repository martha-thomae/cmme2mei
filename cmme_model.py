from abc import ABC
from typing import List, Optional

from cmme_model_events import Event


# .................. GENERAL DATA ............................
class SourceInfo:
    def __init__(self, name: str, id_: int):
        self.name = name
        self.id_ = id_


class VariantVersion:
    def __init__(self, id_: str, source: Optional[SourceInfo] = None, description: Optional[str] = None,
                 missing_voices: Optional[List[str]] = None):
        self.id_ = id_
        self.source = source
        self.description = description
        self.missing_voices = missing_voices if missing_voices is not None else []


class ColorAndFillData:
    """
    Represents the ColorAndFillData group, which contains a Color and Fill element.
    """

    def __init__(self, color: Optional[str] = None, fill: Optional[str] = None):
        self.color = color
        self.fill = fill


class ColorationData:
    """
    Represents the data for coloration, including primary and secondary ColorAndFillData.
    """

    def __init__(self, primary_color: ColorAndFillData, secondary_color: Optional[ColorAndFillData] = None):
        self.primary_color = primary_color
        self.secondary_color = secondary_color


class BaseColoration:
    """
    Represents the BaseColoration element, which contains ColorationData.
    """

    def __init__(self, coloration_data: ColorationData):
        self.coloration_data = coloration_data


class GeneralData:
    def __init__(self, incipit: Optional[str], title: str, section: Optional[str], composer: str, editor: str,
                 publicNotes: Optional[str], notes: Optional[str], variant_versions: List[VariantVersion],
                 base_coloration: Optional[BaseColoration] = None):
        self.incipit = incipit
        self.title = title
        self.section = section
        self.composer = composer
        self.editor = editor
        self.publicNotes = publicNotes
        self.notes = notes
        self.variant_versions = variant_versions
        self.base_coloration = base_coloration


# .................. VOICE DATA ............................
class SingleVoiceData:
    """
    Represents the data for a single voice.
    """

    def __init__(self, name: str, editorial: Optional[str] = None, canon_resolutio: Optional[str] = None,
                 suggested_modern_clef: Optional[str] = None):
        self.name = name
        self.editorial = editorial
        self.canon_resolutio = canon_resolutio
        self.suggested_modern_clef = suggested_modern_clef


class VoiceData:
    """
    Represents the VoiceData, which includes NumVoices and a list of Voice objects.
    """

    def __init__(self, num_voices: int, voices: Optional[List[SingleVoiceData]] = None):
        self.num_voices = num_voices
        self.voices = voices if voices is not None else []


# .................. MUSIC SECTION ............................


class EventList:
    """
    Represents the events inside a Voice, such as Clef, Note, Rest, or complex structures like VariantReadings or EditorialData.
    """

    def __init__(self, events: List[Event]):
        self.events = events


class Voice:
    """
    Represents a voice in the MensuralMusic, Plainchant, or TextSection.
    Each voice has a VoiceNum, an optional list of MissingVersionID, and an EventList.
    """

    def __init__(self, voice_num: int, missing_version_ids: Optional[List[str]], event_list: EventList):
        self.voice_num = voice_num
        self.missing_version_ids = missing_version_ids if missing_version_ids is not None else []
        self.event_list = event_list


class AbstractMusicSectionContent(ABC):
    """
    A generic class that is inherited by MensuralMusic, Plainchant, and TextSection.
    It includes NumVoices and a list of Voice objects.
    """

    def __init__(self, section_type: str, num_voices: int, voices: List[Voice]):
        self.section_type = section_type  # "MensuralMusic", "Plainchant", "Text"
        self.num_voices = num_voices
        self.voices = voices


class TacetData:
    """
    Represents the TacetData group, which contains VoiceNum and TacetText elements.
    """

    def __init__(self, voice_num: int, tacet_text: str):
        self.voice_num = voice_num
        self.tacet_text = tacet_text


class MensuralMusic(AbstractMusicSectionContent):
    """
    Represents the MensuralMusic section.
    Inherits from AbstractMusicSectionContent.
    """

    def __init__(self, num_voices: int, base_coloration: Optional[BaseColoration],
                 tacet_instructions: Optional[List[TacetData]], voices: List[Voice]):
        super().__init__('MensuralMusic', num_voices, voices)
        self.base_coloration = base_coloration
        self.tacet_instructions = tacet_instructions if tacet_instructions is not None else []


class Plainchant(AbstractMusicSectionContent):
    """
    Represents the Plainchant section.
    Inherits from AbstractMusicSectionContent.
    """

    def __init__(self, num_voices: int, base_coloration: Optional[BaseColoration],
                 tacet_instructions: Optional[List[TacetData]], voices: List[Voice]):
        super().__init__('Plainchant', num_voices, voices)
        self.base_coloration = base_coloration
        self.tacet_instructions = tacet_instructions if tacet_instructions is not None else []


class TextSection(AbstractMusicSectionContent):
    """
    Represents the Text section.
    Inherits from MusicPart.
    """

    def __init__(self, num_voices: int, voices: List[Voice]):
        super().__init__('Text', num_voices, voices)


class MusicSection:
    def __init__(self, content: AbstractMusicSectionContent):
        self.content = content


# .................. PIECE ............................
class Piece:
    def __init__(self, cmme_version: float, general_data: GeneralData, voice_data: VoiceData,
                 music_sections: List[MusicSection]):
        self.cmme_version = cmme_version
        self.general_data = general_data
        self.voice_data = voice_data
        self.music_sections = music_sections
