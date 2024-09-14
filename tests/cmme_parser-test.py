import unittest
import os

from model import Piece
from model.clef import ClefEvent
from model.events import EventAttributes
from model.mensuration import MensurationEvent
from model.modern_text import ModernText
from model.note import NoteEvent
from model.pitch import Pitch
from model.original_text import OriginalTextEvent


class TestCMMEImporter(unittest.TestCase):
    def import_score(self, filename):
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources', filename)
        with open(self.resource_path) as file:
            file_contents = file.read()
            piece = Piece.parse(file_contents)
        self.assertIsNotNone(piece)
        return piece

    def test_import_score_BrusBRIV922(self):
        piece = self.import_score('Anonymous-CibavitEos-BrusBRIV922.cmme.xml')

        # Test CMME version
        self.assertEqual("0.897", piece.cmme_version)

        # Test general data
        general_data = piece.general_data
        self.assertEqual("Cibavit eos", general_data.title)
        self.assertEqual("Anonymous", general_data.composer)
        self.assertEqual("Frans Wiering", general_data.editor)
        self.assertIn("Maximae to longae", general_data.notes)  # Ensure specific note text is present

        # Test variant versions
        variant_versions = general_data.variant_versions
        self.assertEqual(2, len(variant_versions))
        self.assertEqual("Wiering", variant_versions[0].id_)
        self.assertEqual("BrusBR IV.922", variant_versions[0].source.name)
        self.assertEqual("Occo Codex", variant_versions[1].id_)

        # Test voice data
        voice_data = piece.voice_data
        self.assertEqual(4, voice_data.num_voices)
        self.assertEqual("[Superius]", voice_data.voices[0].name)
        self.assertEqual("Contra[tenor]", voice_data.voices[1].name)
        self.assertEqual("Tenor", voice_data.voices[2].name)
        self.assertEqual("Bassus", voice_data.voices[3].name)

        # Test section types
        music_sections = piece.music_sections
        self.assertEqual(6, len(music_sections))
        for i in range(3):
            self.assertEqual("Plainchant", music_sections[i * 2].content.section_type)
            self.assertEqual("MensuralMusic", music_sections[i * 2 + 1].content.section_type)

        # Test music section
        # First: plainchant section
        plainchant = music_sections[0].content
        self.assertEqual("Plainchant", plainchant.section_type)  # already tested above
        self.assertEqual(1, plainchant.num_voices)
        self.assertEqual(1, len(plainchant.voices))

        plainchant_events = plainchant.voices[0].event_list.events
        self.assertEqual(10, len(plainchant.voices[0].event_list.events))

        # Directly comparing objects using __eq__ method
        expected_clef_event = ClefEvent(appearance='Bmol', staff_loc=6, pitch=Pitch('B', 3), signature=True, event_attributes=EventAttributes(colored=True))
        self.assertEqual(expected_clef_event, plainchant_events[1])

        expected_original_text_event = OriginalTextEvent(phrase='Cibauit.')
        self.assertEqual(expected_original_text_event, plainchant_events[2])

        expected_mensuration_event = MensurationEvent(
            main_symbol='C',
            strokes=1,
            orientation=None,  # If orientation is optional
            dot=False,
            number=None,  # If no number is provided
            staff_loc=None,  # If staff_loc is optional
            mens_info={},  # Empty dict if no mens_info is provided
            no_score_effect=False,
            event_attributes=EventAttributes()  # Assuming default EventAttributes
        )
        self.assertEqual(expected_mensuration_event, plainchant_events[3])

        # Updated Note Event with new constructor
        expected_note_event = NoteEvent(
            note_type='Brevis',
            pitch=Pitch(letter_name='F', octave_num=2),  # Pitch object
            lig='Recta',  # Lig attribute from the XML
            stem_dir=None,  # No stem direction provided in the XML snippet
            modern_text=ModernText(syllables=['ba'], has_word_end=False)  # ModernText with syllables
        )
        self.assertEqual(expected_note_event, plainchant_events[5])


        # Second: mensural section
        mensural = music_sections[1].content
        self.assertEqual("MensuralMusic", mensural.section_type)  # already tested above
        self.assertEqual(4, mensural.num_voices)
        self.assertEqual(4, len(mensural.voices))

        mensural_basssus_events = mensural.voices[3].event_list.events
        #self.assertEqual(161, len(mensural_basssus_events)) TO-DO Check it

        #TO-DO Finish checking it


if __name__ == '__main__':
    unittest.main()
