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
import UnittestExtensions as ute

sys.path.append("../")

import State
import WarBot

np.random.seed(0) # Needed in order to get "predictable" results.
TEST_FILENAME = "worlds/Testland/states.json"
TEST_PLAYERS = {
    "A": {
        "pop": 10000,
        "area": 2000,
        "id": 1,
        "neighbors": ["B"],
        "growth_rate": 0.01,
        "name": "A"
    },
    "B": {
        "pop": 20000,
        "area": 1000,
        "id": 2,
        "neighbors": ["A"],
        "growth_rate": -0.01,
        "name": "B"
    }
}

class test_WarBot(ut.TestCase):
    def setUp(self):
        self._wb = WarBot.WarBot(TEST_FILENAME)


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
                self.assertFalse(ll in pp.get_neighbors())


    def test_merge_players(self):
        """Test merge_players() method"""

        loser = "A"
        winner = "B"
        self._wb.merge_players(winner, loser)

        self.assertFalse(loser in self._wb._players.keys())


    @ut.skip("OK")
    def test_run(self):
        """Test run() method: SKIP due to printing"""

        pass


    @ut.skip("OK")
    def test_print_players(self):
        """Test print_players() method: SKIP as non-functional."""

        pass


    def test_compute_world_population(self):
        """Test compute_world_population() method"""

        er = sum([tp["pop"] for tp in TEST_PLAYERS.values()])
        cr = self._wb.compute_world_population()

        self.assertEqual(er, cr)


    @ut.skip("OK")
    def test_get_history(self):
        """Test get_history() method: SKIP"""

        pass


    def test_update_history(self):
        """Test update_history method: SKIP - NotImplemented yet. Need to find
        suitable test cases."""

        # TODO: implement suitable test-cases
        NotImplemented


    def test_compute_battle_strengths(self):
        """Test compute_battle_strengths() staticmethod"""

        subtests = []
        battle_pair_keys = ["A", "B"]
        battle_pair = [self._wb._players[bpk] for bpk in battle_pair_keys]

        subtests.append({
            "arg": battle_pair,
            "kwarg": {"method": "poparea"},
            "er": [7. / 18, 11. / 18],
            "msg": "Testing 'poparea' method."
        })

        for ii, sbt in enumerate(subtests):
            with self.subTest(i = ii, msg = sbt["msg"]):
                cr = self._wb.compute_battle_strengths(sbt["arg"], **sbt["kwarg"])
                self.assertAlmostEqual(sbt["er"], cr, places = 4)
                self.assertAlmostEqual(sum(cr), 1., places = 4)


    def test_update_populations_after_battle(self):
        """Test post-battle population update"""

        pks = ["A", ]
        pls = [100, ]
        er = self._wb._players[pks[0]].get_population() - pls[0]

        self._wb.update_populations_after_battle(pks, pls)

        self.assertEqual(er, self._wb._players[pks[0]].get_population())



    def test_compute_fatalities(self):
        """Test compute_fatalities() staticmethod"""

        # TODO This test needs to be extended as it does not cover all cases yet
        pop = 1000
        rs = 0.5
        bo = 0.5

        er = pop // 2
        cr = self._wb.compute_fatalities(pop, rs, bo)

        self.assertEqual(er, cr)


    def test_update_populations_of_non_battling_states(self):
        """Test update_populations_of_non_battling_states()"""

        battling_states = ["A", ]
        self._wb.update_populations_of_non_battling_states(battling_states)
        cr = self._wb._players["B"].get_population()
        state = State.State(TEST_PLAYERS["B"])
        state.grow()
        er = state.get_population()

        self.assertEqual(er, cr)
