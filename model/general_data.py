from typing import List, Optional
from xml.etree.ElementTree import Element

from model.coloration import BaseColoration

class SourceInfo:
    def __init__(self, name: str, id_: int):
        self.name = name
        self.id_ = id_

    @classmethod
    def parse(cls, element: Element) -> Optional['SourceInfo']:
        if element is None:
            return None

        name_el = element.find('{http://www.cmme.org}Name')
        id_el = element.find('{http://www.cmme.org}ID')

        name = name_el.text if name_el is not None else None
        id_ = int(id_el.text) if id_el is not None else None

        return cls(name, id_)  # Return an instance of SourceInfo

class VariantVersion:
    def __init__(self, id_: str, source: Optional[SourceInfo] = None, description: Optional[str] = None,
                 missing_voices: Optional[List[str]] = None):
        self.id_ = id_
        self.source = source
        self.description = description
        self.missing_voices = missing_voices if missing_voices is not None else []

    @classmethod
    def parse(cls, element: Element) -> 'VariantVersion':
        id_el = element.find('{http://www.cmme.org}ID')
        id_ = id_el.text if id_el is not None else None

        source_el = element.find('{http://www.cmme.org}Source')
        source = SourceInfo.parse(source_el) if source_el is not None else None

        description_el = element.find('{http://www.cmme.org}Description')
        description = description_el.text if description_el is not None else None

        missing_voices_el = element.find('{http://www.cmme.org}MissingVoices')
        missing_voices = []
        if missing_voices_el is not None:
            voice_num_els = missing_voices_el.findall('{http://www.cmme.org}VoiceNum')
            missing_voices = [voice_num_el.text for voice_num_el in voice_num_els if voice_num_el.text is not None]

        return cls(id_, source, description, missing_voices)



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

    @classmethod
    def parse(cls, element) -> 'GeneralData':
        if element is None:
            raise ValueError("GeneralData element is missing")

        incipit_el = element.find('{http://www.cmme.org}Incipit')
        incipit = incipit_el.text if incipit_el is not None else None

        title_el = element.find('{http://www.cmme.org}Title')
        title = title_el.text if title_el is not None else None

        section_el = element.find('{http://www.cmme.org}Section')
        section = section_el.text if section_el is not None else None

        composer_el = element.find('{http://www.cmme.org}Composer')
        composer = composer_el.text if composer_el is not None else None

        editor_el = element.find('{http://www.cmme.org}Editor')
        editor = editor_el.text if editor_el is not None else None

        publicNotes_el = element.find('{http://www.cmme.org}PublicNotes')
        publicNotes = publicNotes_el.text if publicNotes_el is not None else None

        notes_el = element.find('{http://www.cmme.org}Notes')
        notes = notes_el.text if notes_el is not None else None

        # Parse BaseColoration
        base_coloration_el = element.find('{http://www.cmme.org}BaseColoration')
        base_coloration = BaseColoration.parse(base_coloration_el)

        # Handle 0..* (unbounded) cardinality for VariantVersion
        variant_versions = [VariantVersion.parse(var_ver_el) for var_ver_el in
                            element.findall('{http://www.cmme.org}VariantVersion')]

        return cls(incipit, title, section, composer, editor, publicNotes, notes, variant_versions, base_coloration)
