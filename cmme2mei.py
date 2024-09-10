"""
Author: David Rizo
Original Java Code Author: David Rizo (drizo@dlsi.ua.es)
Python Conversion Date: 05/20/2019
Last Modified By: [Your Name], [Date]
Version: 1.0.0

Changelog:
    Version 1.0.0 - [Date] - Initial conversion from Java to Python.
    - Implemented XML parsing using ElementTree.
    - Added support for importing metadata, voice data, plainchant, and mensural music.
    - Methods for importing notes, rests, clefs, and other musical events were added - not finished (just printing information).

Contributors:
    - [Contributor 1 Name], [Date], Changes: [Description of changes]
    - [Contributor 2 Name], [Date], Changes: [Description of changes]
"""

import xml.etree.ElementTree as ET

NAMESPACE = {'cmme': 'http://www.cmme.org'}


class ImportException(Exception):
    pass

class Score:
    def __init__(self):
        self.metadata = None
        self.voices = []
        self.staves = []

class Metadata:
    def __init__(self, title=None, composer=None, editor=None, comments=None):
        self.title = title
        self.composer = composer
        self.editor = editor
        self.comments = comments

class Voice:
    def __init__(self, name):
        self.name = name
        self.events = []

class Staff:
    def __init__(self, name):
        self.name = name
        self.elements = []

class CMMEImporter:
    FIGURES_MAP = {
        "Maxima": "MAXIMA",
        "Longa": "LONGA",
        "Brevis": "BREVIS",
        "Semibrevis": "SEMIBREVE",
        "Minima": "MINIM",
        "Semiminima": "SEMIMINIM",
        "Fusa": "FUSA",
    }

    def __init__(self):
        self.variant_id = "DEFAULT"
        self.score = Score()
        self.voices_in_section = set()

    def set_variant_id(self, variant_id):
        self.variant_id = variant_id

    def import_score(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self.import_metadata_and_create_score(root)
            self.import_voice_data(root)
            self.import_sections(root)
            return self.score
        except Exception as e:
            raise ImportException(e)

    def import_metadata_and_create_score(self, root):
        general_data = root.find('{http://www.cmme.org}GeneralData')
        title = general_data.find('{http://www.cmme.org}Title').text if general_data is not None else None
        composer = general_data.find('{http://www.cmme.org}Composer').text if general_data is not None else None
        editor = general_data.find('{http://www.cmme.org}Editor').text if general_data is not None else None
        notes = general_data.find('{http://www.cmme.org}Notes').text if general_data is not None else None

        self.score.metadata = Metadata(title, composer, editor, notes)

    def import_voice_data(self, root):
        voice_data = root.find('{http://www.cmme.org}VoiceData')
        voices = voice_data.findall('{http://www.cmme.org}Voice') if voice_data is not None else []
        self.score.voices = [Voice(voice.find('{http://www.cmme.org}Name').text) for voice in voices]
        self.score.staves = [Staff(voice.find('{http://www.cmme.org}Name').text) for voice in voices]

    def import_sections(self, root):
        sections = root.findall('{http://www.cmme.org}MusicSection')
        for section in sections:
            if section.find('{http://www.cmme.org}Plainchant') is not None:
                self.import_plainchant(section.find('{http://www.cmme.org}Plainchant'))
            if section.find('{http://www.cmme.org}MensuralMusic') is not None:
                self.import_mensural_music(section.find('{http://www.cmme.org}MensuralMusic'))

    def import_plainchant(self, plainchant):
        self.voices_in_section.clear()
        voices = plainchant.findall('{http://www.cmme.org}Voice')
        for voice in voices:
            voice_num = int(voice.find('{http://www.cmme.org}VoiceNum').text) - 1
            self.add_notation_type_if_required(voice_num, "PlainChant")
            self.import_voice(voice_num, voice.find('{http://www.cmme.org}EventList'))

    def import_mensural_music(self, mensural_music):
        self.voices_in_section.clear()
        voices = mensural_music.findall('{http://www.cmme.org}Voice')
        for voice in voices:
            voice_num = int(voice.find('{http://www.cmme.org}VoiceNum').text) - 1
            self.add_notation_type_if_required(voice_num, "Mensural")
            self.import_voice(voice_num, voice.find('{http://www.cmme.org}EventList'))

    def add_notation_type_if_required(self, voice_num, notation_type):
        if voice_num not in self.voices_in_section:
            self.voices_in_section.add(voice_num)
            self.score.staves[voice_num].elements.append(f"NotationType: {notation_type}")

    def import_voice(self, voice_num, event_list):
        events = list(event_list)
        for event in events:
            self.process_event(voice_num, event)

    def process_event(self, voice_num, event):
        event_tag = event.tag.split('}')[1]
        if event_tag == "VariantReadings":
            self.import_variants(voice_num, event)
        elif event_tag == "Clef":
            self.import_clef(voice_num, event)
        elif event_tag == "Mensuration":
            self.import_mensuration(voice_num, event)
        elif event_tag == "Note":
            self.import_note(voice_num, event)
        elif event_tag == "Rest":
            self.import_rest(voice_num, event)
        elif event_tag == "Dot":
            self.import_dot(voice_num, event)
        elif event_tag == "Proportion":
            self.import_proportion(voice_num, event)
        elif event_tag == "Custos":
            self.import_custos(voice_num, event)
        elif event_tag == "OriginalText":
            self.import_original_text(voice_num, event)
        elif event_tag == "MiscItem":
            self.import_misc_item(voice_num, event)
        elif event_tag == "LineEnd":
            self.import_line_end(voice_num, event)
        else:
            print(f"Unsupported event: {event_tag}")

    def import_note(self, voice_num, event):
        note_type = event.find('{http://www.cmme.org}Type').text
        pitch = event.find('{http://www.cmme.org}Pitch').text if event.find('{http://www.cmme.org}Pitch') is not None else 'Unknown'
        octave = event.find('{http://www.cmme.org}Octave').text if event.find('{http://www.cmme.org}Octave') is not None else 'Unknown'
        print(f"Note imported in voice {voice_num}: Type = {note_type}, Pitch = {pitch}, Octave = {octave}")

    def import_rest(self, voice_num, event):
        rest_type = event.find('{http://www.cmme.org}Type').text
        print(f"Rest imported in voice {voice_num}: Type = {rest_type}")

    def import_clef(self, voice_num, event):
        clef_type = event.find('{http://www.cmme.org}Appearance').text if event.find('{http://www.cmme.org}Appearance') is not None else 'Unknown'
        staff_loc = event.find('{http://www.cmme.org}StaffLoc').text if event.find('{http://www.cmme.org}StaffLoc') is not None else 'Unknown'
        print(f"Clef imported in voice {voice_num}: Clef Type = {clef_type}, Staff Location = {staff_loc}")

    def import_mensuration(self, voice_num, event):
        mensuration_type = event.find('{http://www.cmme.org}Sign').find('{http://www.cmme.org}MainSymbol').text if event.find('{http://www.cmme.org}Sign') is not None else 'Unknown'
        print(f"Mensuration imported in voice {voice_num}: Type = {mensuration_type}")

    def import_dot(self, voice_num, event):
        print(f"Dot imported in voice {voice_num}")

    def import_proportion(self, voice_num, event):
        print(f"Proportion imported in voice {voice_num}")

    def import_custos(self, voice_num, event):
        custos_pitch = event.find('{http://www.cmme.org}LetterName').text if event.find('{http://www.cmme.org}LetterName') is not None else 'Unknown'
        custos_octave = event.find('{http://www.cmme.org}OctaveNum').text if event.find('{http://www.cmme.org}OctaveNum') is not None else 'Unknown'
        print(f"Custos imported in voice {voice_num}: Pitch = {custos_pitch}, Octave = {custos_octave}")

    def import_original_text(self, voice_num, event):
        text = event.text if event is not None else 'No text'
        print(f"Original text imported in voice {voice_num}: {text}")

    def import_misc_item(self, voice_num, event):
        print(f"Miscellaneous item imported in voice {voice_num}")

    def import_line_end(self, voice_num, event):
        print(f"Line end imported in voice {voice_num}")

    def import_variants(self, voice_num, event):
        # Assuming VariantReadings has a structure with Readings inside
        readings = event.findall('{http://www.cmme.org}Reading')
        for reading in readings:
            variant_versions = reading.findall('{http://www.cmme.org}VariantVersionID')
            variant_text = reading.find('{http://www.cmme.org}Music').text if reading.find('{http://www.cmme.org}Music') is not None else 'No Music Data'

            # Collect the variant version IDs
            version_ids = [variant_version.text for variant_version in variant_versions]
            version_str = ', '.join(version_ids)

            print(f"Variant reading for voice {voice_num}: Versions = {version_str}, Music = {variant_text}")
