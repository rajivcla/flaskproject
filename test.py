import unittest
from app import app

class VSNTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_bad_format(self):
        with self.client as c:
            result = c.get('/1')
            self.assertEqual(result.json['error'],'input not in the correct format, 6 letters followed by 6 numbers')
    
    def test_good_VSN(self):
        with self.client as c:
            result = c.get('XXRCXV123456')
            self.assertNotEqual(result.json['result'], 'no match found')
            self.assertEqual(result.json['result'],'XXRC*V******')
    
    def test_no_match(self):
        with self.client as c:
            result = c.get('ZXRCXV123456')
            self.assertEqual(result.json['result'], 'no match found')
    
    def test_closest_match(self):
        with self.client as c:
            result = c.get('XXRCXV123436')
            self.assertEqual(result.json['result'], 'XXRC*V****3*')

if __name__ == '__main__':
    unittest.main()