#!/usr/bin/env python3
"""
    Testing WarBot Object
    =====================

    Each and every method must have its designated test.

"""

import sys
import numpy as np
import unittest as ut

sys.path.append("../")

import warbot

np.random.seed(0) # Needed in order to get "predictable" results.
TEST_FILENAME = "test_data.json"

class test_warbot(ut.TestCase):
    def setUp(self):
        self._wb = warbot.WarBot(TEST_FILENAME)


    def test_load_players(self):
        """Test load_players() method"""

        cr = self._wb.load_players(TEST_FILENAME) # In a way redundant, but this is what we actually wanna test here.
        er = {
            "A": {
                "pop": 10000,
                "area": 2000,
                "id": 1,
                "neighbors": ["B"]
            },
            "B": {
                "pop": 20000,
                "area": 1000,
                "id": 2,
                "neighbors": ["A"]
            }
        }

        self.assertEqual(cr, er)


    def test_compute_round(self):
        """Test compute_round() method"""

        self._wb.compute_round()
        self.assertEqual(self._wb._n_of_rounds, 1)
        self.assertEqual(self._wb._players_names, ["B", ])


    def test_get_pairs(self):
        """Test get_pairs() method"""

        cr = self._wb.get_pairs()
        er = [["B", "A"]] # WARNING order depends on random seed!

        self.assertEqual(cr, er)


    def test_compute_battles(self):
        """Test compute_battles() method"""

        battle_pairs = [["A", "B"], ]
        self._wb.compute_battles(battle_pairs)
        cl = self._wb._losers
        el = ["B", ]
        self.assertEqual(cl, el)


    def test_clean_neighborhoods(self):
        """Test clean_neighborhoods() method"""

        losers = ["A", ]
        winners = ["B", ]

        self._wb.clean_neighborhoods(losers, winners)
        for ll in losers:
            for pp in self._wb._players.values():
                self.assertFalse(ll in pp["neighbors"])


    def test_merge_players(self):
        """Test merge_players() method"""

        loser = "A"
        winner = "B"

        self._wb.merge_players(winner, loser)
        er = {'B': {'pop': 30000, 'area': 3000, 'id': 2, 'neighbors': []}}
        self.assertEqual(er, self._wb._players)


    @ut.skip("OK")
    def test_run(self):
        """Test run() method: SKIP due to printing"""

        pass


    @ut.skip("OK")
    def test_print_players(self):
        """Test print_players() method: SKIP as non-functional."""

        pass
