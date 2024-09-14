import unittest
import os

from cmme_model_events import EventAttributes
from cmme_parser import PieceParser


class TestCMMEImporter(unittest.TestCase):
    def setUp(self):
        self.importer = PieceParser()

    def check_event_attributes(self, event_attributes, expected_attributes):
        """
        Helper method to check EventAttributes fields.
        """
        self.assertEqual(expected_attributes.colored, event_attributes.colored, "Incorrect 'colored' attribute")
        self.assertEqual(expected_attributes.ambiguous, event_attributes.ambiguous, "Incorrect 'ambiguous' attribute")
        self.assertEqual(expected_attributes.editorial, event_attributes.editorial, "Incorrect 'editorial' attribute")
        self.assertEqual(expected_attributes.error, event_attributes.error, "Incorrect 'error' attribute")
        self.assertEqual(expected_attributes.editorial_commentary, event_attributes.editorial_commentary, "Incorrect 'editorial_commentary' attribute")

    def check_clef_event(self, clef_event, expected_appearance, expected_staff_loc, expected_letter_name, expected_octave_num, expected_signature=False, expected_event_attributes=None):
        """
        Helper method to check ClefEvent attributes.
        """
        # Ensure the event type is 'Clef'
        self.assertEqual('Clef', clef_event.event_type)

        # Check Clef attributes
        self.assertEqual(expected_appearance, clef_event.appearance, "Incorrect Clef appearance")
        self.assertEqual(expected_staff_loc, clef_event.staff_loc, "Incorrect Clef staff location")

        # Check Pitch attributes
        self.assertEqual(expected_letter_name, clef_event.pitch.letter_name, "Incorrect Clef pitch letter name")
        self.assertEqual(expected_octave_num, clef_event.pitch.octave_num, "Incorrect Clef pitch octave number")

        # Check Signature
        self.assertEqual(expected_signature, clef_event.signature, "Incorrect Clef signature status")

        # Check EventAttributes (if provided)
        if expected_event_attributes:
            self.check_event_attributes(clef_event.event_attributes, expected_event_attributes)

    def check_original_text_event(self, original_text_event, expected_phrase):
        """
        Helper method to check OriginalTextEvent attributes.
        """
        self.assertEqual('OriginalText', original_text_event.event_type)  # Ensure the event type is 'OriginalText'

        # Check Phrase attribute
        self.assertEqual(expected_phrase, original_text_event.phrase, "Incorrect OriginalText phrase")

    def check_mensuration_event(self, mensuration_event, expected_main_symbol, expected_strokes):
        """
        Helper method to check MensurationEvent attributes.
        """
        self.assertEqual('Mensuration', mensuration_event.event_type)  # Ensure the event type is 'Mensuration'

        # Check Sign attributes
        self.assertEqual(expected_main_symbol, mensuration_event.main_symbol, "Incorrect MainSymbol in Mensuration")
        self.assertEqual(expected_strokes, mensuration_event.strokes, "Incorrect Strokes in Mensuration")

    def check_note_event(self, note_event, expected_type, expected_letter_name, expected_octave_num, expected_lig=None, expected_syllable=None, expected_length_num=None, expected_length_den=None):
        """
        Helper method to check NoteEvent attributes.
        """
        self.assertEqual('Note', note_event.event_type)  # Ensure the event type is 'Note'

        # Check Note attributes
        self.assertEqual(expected_type, note_event.note_type, "Incorrect Note type")
        self.assertEqual(expected_letter_name, note_event.letter_name, "Incorrect Note letter name")
        self.assertEqual(expected_octave_num, note_event.octave_num, "Incorrect Note octave number")

        # Check optional Lig
        if expected_lig:
            self.assertEqual(expected_lig, note_event.lig, "Incorrect Note ligature type")

        # Check optional Syllable
        if expected_syllable:
            self.assertEqual(expected_syllable, note_event.syllable, "Incorrect ModernText syllable")

        # Check optional Length (if provided)
        if expected_length_num and expected_length_den:
            self.assertEqual(expected_length_num, note_event.length_num, "Incorrect Note length numerator")
            self.assertEqual(expected_length_den, note_event.length_den, "Incorrect Note length denominator")

    def check_mensuration_event(self, mensuration_event, expected_main_symbol, expected_orientation=None,
                                expected_strokes=None, expected_dot=False, expected_staff_loc=None,
                                expected_mens_info=None, expected_no_score_effect=False, expected_event_attributes=None):
        """
        Helper method to check MensurationEvent attributes.
        """
        self.assertEqual('Mensuration', mensuration_event.event_type)

        # Check Mensuration attributes
        self.assertEqual(expected_main_symbol, mensuration_event.main_symbol, "Incorrect Mensuration main symbol")
        self.assertEqual(expected_orientation, mensuration_event.orientation, "Incorrect Mensuration orientation")
        self.assertEqual(expected_strokes, mensuration_event.strokes, "Incorrect Mensuration strokes")
        self.assertEqual(expected_dot, mensuration_event.dot, "Incorrect Mensuration dot")
        self.assertEqual(expected_staff_loc, mensuration_event.staff_loc, "Incorrect Mensuration staff location")

        # Check MensInfo attributes if provided
        if expected_mens_info:
            self.assertEqual(expected_mens_info, mensuration_event.mens_info, "Incorrect Mensuration mens info")

        # Check NoScoreEffect
        self.assertEqual(expected_no_score_effect, mensuration_event.no_score_effect, "Incorrect NoScoreEffect status")

        # Check EventAttributes (if provided)
        if expected_event_attributes:
            self.check_event_attributes(mensuration_event.event_attributes, expected_event_attributes)


    def import_score(self, filename):
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources', filename)
        with open(self.resource_path) as file:
            file_contents = file.read()
            piece = self.importer.parse_piece(file_contents)
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
            self.assertEqual("Plainchant", music_sections[i*2].content.section_type)
            self.assertEqual("MensuralMusic", music_sections[i*2+1].content.section_type)

        # Test music section
        # First: plain chant section
        plainchant = music_sections[0].content
        self.assertEqual("Plainchant", plainchant.section_type) # already tested above
        self.assertEqual(1, plainchant.num_voices)
        self.assertEqual(1, len(plainchant.voices))

        plainchant_events = plainchant.voices[0].event_list.events
        self.assertEqual(10, len(plainchant.voices[0].event_list.events))
        self.check_clef_event(
            clef_event=plainchant_events[1],
            expected_appearance='Bmol',
            expected_staff_loc=6,
            expected_letter_name='B',
            expected_octave_num=3,
            expected_signature=True,
            expected_event_attributes=EventAttributes(colored=True)  # 'Colored' attribute set to True
        )

        self.check_original_text_event(
            original_text_event=plainchant_events[2],  # Assuming the OriginalText event is at index 1
            expected_phrase='Cibauit.'
        )

        self.check_mensuration_event(
            mensuration_event=plainchant_events[3],
            expected_main_symbol='C',
            expected_strokes=1
        )

        self.assertEqual('Note', plainchant_events[4].event_type)


        self.assertEqual('Note', plainchant_events[6].event_type)
        self.assertEqual('Dot', plainchant_events[7].event_type)
        self.assertEqual('Note', plainchant_events[8].event_type)
        self.assertEqual('MiscItem', plainchant_events[9].event_type)

        # Second: mensural section
        mensural = music_sections[1].content
        self.assertEqual("MensuralMusic", mensural.section_type) # already tested above
        self.assertEqual(4, mensural.num_voices)
        self.assertEqual(4, len(mensural.voices))
        mensural_basssus_events = mensural.voices[3].event_list.events
        self.assertEqual('Clef', mensural_basssus_events[0].event_type)
        self.assertEqual('MultiEvent', mensural_basssus_events[1].event_type)
        self.assertEqual('OriginalText', mensural_basssus_events[2].event_type)
        self.assertEqual('Note', mensural_basssus_events[3].event_type)
        self.assertEqual('Note', mensural_basssus_events[4].event_type)
        self.assertEqual('Rest', mensural_basssus_events[5].event_type)
        self.assertEqual('Rest', mensural_basssus_events[6].event_type)


if __name__ == '__main__':
    unittest.main()
