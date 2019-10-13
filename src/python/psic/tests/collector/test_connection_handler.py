from os import path
from typing import List
from unittest import TestCase

from psic.collector.connection_handler import ConnectionHandler
from psic.collector.storm import Storm

SELF_PATH = path.dirname(path.abspath(__file__))


class TestConnectionHandler(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(SELF_PATH)
        cls.c = ConnectionHandler(html_text=open(path.join(SELF_PATH, 'resources/'
                                                 'Storms_List_Page.html'), 'r').read())

    def test_generate_storm_list_all(self):

        # Parse all 34 storms
        self.assertEqual(len(self.c.generate_storm_list()), 34)

    def test_generate_storm_list_search_year(self):

        # Parse all 2008 storms (2)
        self.assertEqual(len(self.c.generate_storm_list(search_re='2008')), 2)

    def test_generate_storm_list_search_name_term(self):

        # Parse all hurricanes (25)
        self.assertEqual(len(self.c.generate_storm_list(search_re='hurricane')), 25)

    def test_generate_storm_list_search_none(self):

        # Test when there are no matches
        self.assertEqual(len(self.c.generate_storm_list(search_re='no storms will match this')), 0)

    def test_get_storm_list(self):

        # Ensure it actually gets the storm list
        self.assertEqual(self.c.generate_storm_list(), self.c.get_storm_list())

        # Ensure that changing the pattern reloads the cache
        storms_all: List[Storm] = self.c.get_storm_list()
        storms_2019: List[Storm] = self.c.get_storm_list(search_re='2019')
        self.assertNotEqual(storms_all, storms_2019)
