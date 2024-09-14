import unittest
import os

from cmme_parser import PieceParser


class TestCMMEImporter(unittest.TestCase):
    def setUp(self):
        self.importer = PieceParser()

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
        self.assertEqual('Clef', plainchant_events[0].event_type)
        self.assertEqual('Clef', plainchant_events[1].event_type)
        self.assertEqual('OriginalText', plainchant_events[2].event_type)
        self.assertEqual('Mensuration', plainchant_events[3].event_type)
        self.assertEqual('Note', plainchant_events[4].event_type)
        self.assertEqual('Note', plainchant_events[5].event_type)
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
