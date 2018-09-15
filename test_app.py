import unittest
import run
from app import app

class BasicTestCase(unittest.TestCase):
    
    def test_index_route(self):
        """Route Testing for Homepage"""
        indexTest = app.test_client(self)
        response = indexTest.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_leaderboard_route(self):
        """Route Testing for Leaderboard Page"""
        leaderRoute = app.test_client(self)
        response = leaderRoute.get('/leaderboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)    
        
if __name__ == '__main__':
    unittest.main()