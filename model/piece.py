from typing import List
import xml.etree.ElementTree as ET
from .general_data import GeneralData
from .voice_data import VoiceData
from .music_section import MusicSection

class Piece:
    def __init__(self, cmme_version: str, general_data: GeneralData, voice_data: VoiceData,
                 music_sections: List[MusicSection]):
        self.cmme_version = cmme_version
        self.general_data = general_data
        self.voice_data = voice_data
        self.music_sections = music_sections

    @classmethod
    def parse(cls, xml_string: str) -> 'Piece':
        root = ET.fromstring(xml_string)
        cmme_version = root.attrib.get('CMMEversion')

        # Parse GeneralData (required)
        general_data_el = root.find('{http://www.cmme.org}GeneralData')
        general_data = GeneralData.parse(general_data_el)

        # Parse VoiceData (required)
        voice_data_el = root.find('{http://www.cmme.org}VoiceData')
        voice_data = VoiceData.parse(voice_data_el)

        # Parse MusicSection (1..unbounded)
        music_sections = [MusicSection.parse(ms_el) for ms_el in
                          root.findall('{http://www.cmme.org}MusicSection')]

        return Piece(cmme_version, general_data, voice_data, music_sections)

