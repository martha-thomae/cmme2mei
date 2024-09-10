import unittest
import os

from cmme2mei import CMMEImporter


class TestCMMEImporter(unittest.TestCase):
    def setUp(self):
        self.importer = CMMEImporter()

    def import_score(self, filename):
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources', filename)
        score = self.importer.import_score(self.resource_path)
        self.assertIsNotNone(score)
        return score

    def test_import_score(self):
        score = self.import_score('Anonymous-CibavitEos-BrusBRIV922.cmme.xml')

        # Verify metadata
        self.assertEqual(score.metadata.title, "Cibavit eos")
        self.assertEqual(score.metadata.composer, "Anonymous")
        self.assertEqual(score.metadata.editor, "Frans Wiering")

        # Verify voices
        self.assertEqual(len(score.voices), 4)
        self.assertEqual(score.voices[0].name, "[Superius]")

        # Verify some events were imported
        #TO-DO Now they are just (badly) printed - self.assertTrue(any("Note" in event for event in score.voices[0].events))


if __name__ == '__main__':
    unittest.main()
