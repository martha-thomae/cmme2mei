from typing import List, Optional
from xml.etree.ElementTree import Element

from .events import Event

class SingleVoiceData:
    def __init__(self, name: str, editorial: Optional[str] = None, canon_resolutio: Optional[str] = None,
                 suggested_modern_clef: Optional[str] = None):
        self.name = name
        self.editorial = editorial
        self.canon_resolutio = canon_resolutio
        self.suggested_modern_clef = suggested_modern_clef

    @classmethod
    def parse(cls, element: Element) -> 'SingleVoiceData':
        name_el = element.find('{http://www.cmme.org}Name')
        name = name_el.text if name_el is not None else None

        editorial_el = element.find('{http://www.cmme.org}Editorial')
        editorial = editorial_el.text if editorial_el is not None else None

        # Only used in mensural music, not in plainchant. As it's optional, it can be added here
        canon_resolutio_el = element.find('{http://www.cmme.org}CanonResolutio')
        canon_resolutio = canon_resolutio_el.text if canon_resolutio_el is not None else None

        suggested_modern_clef_el = element.find('{http://www.cmme.org}SuggestedModernClef')
        suggested_modern_clef = suggested_modern_clef_el.text if suggested_modern_clef_el is not None else None

        return cls(name, editorial, canon_resolutio, suggested_modern_clef)


class VoiceData:
    def __init__(self, num_voices: int, voices: Optional[List[SingleVoiceData]] = None):
        self.num_voices = num_voices
        self.voices = voices if voices is not None else []

    @classmethod
    def parse(cls, element: Element) -> 'VoiceData':
        # Parse NumVoices (required)
        num_voices_el = element.find('{http://www.cmme.org}NumVoices')
        num_voices = int(num_voices_el.text) if num_voices_el is not None else 0

        # Parse the list of Voice elements
        voices = []
        voice_elements = element.findall('{http://www.cmme.org}Voice')
        for voice_el in voice_elements:
            single_voice_data = SingleVoiceData.parse(voice_el)
            voices.append(single_voice_data)

        return cls(num_voices, voices)

