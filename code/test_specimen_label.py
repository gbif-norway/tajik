import unittest
from specimen_label import SpecimenLabel

def _make_specimen(text, genus='Vulpia'):
    return SpecimenLabel(text, 'TNAS', genus, '123', 'ffd7abab-6509-4bc3-a472-00bf7b49a2ae', 'https://gbif.no/image.jpg')


class ExtractScientificName(unittest.TestCase):
    def test_simple_cases(self):
        tests = [
            'Herbarium БОТАНИКИ\nVulpia alopec\nCollected by A. Person',
            'Herbarium БОТАНИКИ\nБиришти, Vulpia alopec\nCollected by A. Person',
            'Herbarium БОТАНИКИ\nNulpia alopec\nCollected by A. Person',
        ]
        for t in tests:
            label = _make_specimen(t)
            self.assertEqual(label.dwc['verbatimIdentification'], 'Vulpia alopec')
            self.assertEqual(label.label_contents, 'Collected by A. Person')

    def test_different_genus(self):
        label = _make_specimen('Herbarium БОТАНИКИ\nFreesia alopec\nCollected by A. Person')
        self.assertEqual(label.dwc['verbatimIdentification'], 'Freesia alopec')
    
    def test_different_genus_fuzzy(self):
        label = _make_specimen('Herbarium БОТАНИКИ\nFreesio alopec\nCollected by A. Person')
        self.assertEqual(label.dwc['verbatimIdentification'], 'Freesia alopec')

    def test_label_contents_assigned(self):
        label = _make_specimen('Herbarium БОТАНИКИ\nБиришти, Vulpia alopec\nCollected by A. Person')
        self.assertEqual(label.label_contents, 'Collected by A. Person')


class FindHumanName(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()