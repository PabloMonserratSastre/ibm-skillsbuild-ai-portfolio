import tempfile
import unittest
from pathlib import Path
from portfolio import ROOT, load_json, validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.reviews = load_json(ROOT / 'projects/reviews/reference.json')
        self.ids = [r['id'] for r in load_json(ROOT / 'projects/reviews/input.json')]
        self.meeting = load_json(ROOT / 'projects/meeting/reference.json')
        self.security = load_json(ROOT / 'projects/security/reference.json')

    def test_reference_structures(self):
        validate('reviews', self.reviews, self.ids)
        validate('meeting', self.meeting)
        validate('security', self.security)

    def test_missing_review(self):
        self.reviews['reviews'].pop()
        with self.assertRaises(ValueError):
            validate('reviews', self.reviews, self.ids)

    def test_duplicate_review(self):
        self.reviews['reviews'][1]['id'] = 'R1'
        with self.assertRaises(ValueError):
            validate('reviews', self.reviews, self.ids)

    def test_bad_sentiment_type(self):
        self.reviews['reviews'][0]['sentiment'] = ['positive']
        with self.assertRaises(ValueError):
            validate('reviews', self.reviews, self.ids)

    def test_invalid_aspect(self):
        self.reviews['reviews'][0]['aspects'] = ['delivery']
        with self.assertRaises(ValueError):
            validate('reviews', self.reviews, self.ids)

    def test_duplicate_aspects(self):
        self.reviews['reviews'][0]['aspects'] = ['battery', 'battery']
        with self.assertRaises(ValueError):
            validate('reviews', self.reviews, self.ids)

    def test_wrong_action_count(self):
        self.meeting['actions'].pop()
        with self.assertRaises(ValueError):
            validate('meeting', self.meeting)

    def test_impossible_date(self):
        self.meeting['actions'][0]['due'] = '2026-02-30'
        with self.assertRaises(ValueError):
            validate('meeting', self.meeting)

    def test_missing_action_owner(self):
        del self.meeting['actions'][0]['owner']
        with self.assertRaises(ValueError):
            validate('meeting', self.meeting)

    def test_null_date_and_owner_allowed(self):
        self.meeting['actions'][0]['owner'] = None
        self.meeting['actions'][0]['due'] = None
        validate('meeting', self.meeting)

    def test_security_cannot_claim_closed_status(self):
        self.security['status'] = 'resolved'
        with self.assertRaises(ValueError):
            validate('security', self.security)

    def test_security_unknowns_required(self):
        self.security['unknowns'] = []
        with self.assertRaises(ValueError):
            validate('security', self.security)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'response.json'
            path.write_text('{"summary":"a","summary":"b"}', encoding='utf-8')
            with self.assertRaises(ValueError):
                load_json(path)


if __name__ == '__main__':
    unittest.main()
