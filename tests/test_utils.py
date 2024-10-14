import unittest
from utils import helper_function

class TestUtils(unittest.TestCase):

    def test_helper_function(self):
        self.assertEqual(helper_function(2), 4)
        self.assertEqual(helper_function(0), 0)
