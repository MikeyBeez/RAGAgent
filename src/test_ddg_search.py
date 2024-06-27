# tests/test_ddg_search.py

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modules.ddg_search import DDGSearch

class TestDDGSearch(unittest.TestCase):
    def setUp(self):
        self.ddg_search = DDGSearch()

    def test_run_search(self):
        query = "who was Bach?"
        results = self.ddg_search.run_search(query)
        
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("Bach" in result for result in results))

if __name__ == '__main__':
    unittest.main()
