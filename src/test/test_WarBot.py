#!/usr/bin/env python3
"""
    Testing WarBot Object
    =====================

    Each and every method must have its designated test.

"""

import sys
import copy
import numpy as np
import unittest as ut

sys.path.append("../")

import WarBot

np.random.seed(0) # Needed in order to get "predictable" results.
TEST_FILENAME = "worlds/Testland/states.json"
TEST_PLAYERS = {
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

class test_WarBot(ut.TestCase):
    def setUp(self):
        self._wb = WarBot.WarBot(TEST_FILENAME)


    def test_load_players(self):
        """Test load_players() method"""

        cr = self._wb.load_players(TEST_FILENAME) # In a way redundant, but this is what we actually wanna test here.
        er = copy.deepcopy(TEST_PLAYERS)

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


    def test_compute_battle_strengths(self):
        """Test compute_battle_strengths() staticmethod"""

        subtests = []
        battle_pair = [
            {"pop": 10, "area": 10.},
            {"pop": 10, "area": 10.}
        ]

        subtests.append(
            {
                "arg": battle_pair,
                "kwargs": {"method": "poparea"},
                "er": [0.5, 0.5],
                "msg": "Basic usage with 'poparea'"
            }
        )

        subtests.append(
            {
                "arg": battle_pair,
                "kwargs": {"method": "qwertzuiop"},
                "er": [0.5, 0.5],
                "msg": "Invalid method"
            }
        )

        for ii, sbt in enumerate(subtests):
            with self.subTest(i = ii, msg = sbt["msg"]):
                cr = self._wb.compute_battle_strengths(sbt["arg"], **sbt["kwargs"])
                self.assertAlmostEqual(sbt["er"], cr, places = 4)


    def test_update_populations_after_battle(self):
        """Test post-battle population update"""

        self._wb._players = copy.deepcopy(TEST_PLAYERS)
        player_keys = ["A", "B"]
        pop_losses = [100, 200]
        ers = [TEST_PLAYERS[pk]["pop"] - pl for pk, pl in zip(player_keys, pop_losses)]

        self._wb.update_populations_after_battle(player_keys, pop_losses)

        for pk, er in zip(player_keys, ers):
            self.assertEqual(self._wb._players[pk]["pop"], er)


    def test_compute_fatalities(self):
        """Test compute_fatalities() staticmethod"""

        # TODO This test needs to be extended as it does not cover all cases yet
        pop = 1000
        rs = 0.5
        bo = 0.5

        er = pop // 2
        cr = self._wb.compute_fatalities(pop, rs, bo)

        self.assertEqual(er, cr)
