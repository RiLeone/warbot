#!/usr/bin/env python3
"""
    Testing State Module
    ====================

    Each and every method must have its designated test.

"""

import sys
import copy
import logging
import unittest as ut

sys.path.append("../")

import State

TEST_FILENAME = "worlds/Testland/states.json"
TEST_STATES_DICT = {
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


class test_LSFJF(ut.TestCase):
    def setUp(self):
        pass


    def test_load_states_from_json_file(self):
        """Test load_states_from_json_file() function."""

        cr = State.load_states_from_json_file(TEST_FILENAME)
        self.assertEqual(len(cr), 2)

        for state in cr.values():
            self.assertEqual(type(state), type(State.State(TEST_STATES_DICT["A"])))



class test_State(ut.TestCase):
    def setUp(self):
        self._state_A = State.State(copy.deepcopy(TEST_STATES_DICT["A"]))
        self._state_B = State.State(copy.deepcopy(TEST_STATES_DICT["B"]))


    def test_State_constructor(self):
        """Test state constructor."""

        exception_keys = ("_pretty_name", "_history")

        for kk, vv in self._state_A.__dict__.items():
            if kk not in exception_keys:
                self.assertEqual(TEST_STATES_DICT["A"][kk[1:]], vv)


    def test_update_history(self):
        """Test update_history() method."""

        er = 200
        self._state_A._pop = er
        self._state_A.update_history()

        self.assertEqual(er, self._state_A.get_history()["pop"][-1])


    def test_grow(self):
        """Test grow() method."""

        er = TEST_STATES_DICT["A"]["pop"] + self._state_A.compute_population_growth_delta()
        _ = self._state_A.grow()
        self.assertEqual(er, self._state_A.get_history()["pop"][-1])


    def test_compute_population_growth_delta(self):
        """Test test_compute_population_growth_delta() method."""

        er = int(round(TEST_STATES_DICT["A"]["pop"] * TEST_STATES_DICT["A"]["growth_rate"]))

        self.assertEqual(er, self._state_A.compute_population_growth_delta())


    def test_update_populations_after_battle(self):
        """Test update_population_after_battle() method."""

        pop_loss = 100
        er = TEST_STATES_DICT["A"]["pop"] - pop_loss
        self._state_A.update_population_after_battle(100)

        self.assertEqual(er, self._state_A.get_history()["pop"][-1])


    def test_compute_battle_strength(self):
        """Test compute_battle_strength() method."""

        AW, PW = 1., 0.5
        er = TEST_STATES_DICT["A"]["area"] * AW + TEST_STATES_DICT["A"]["pop"] * PW

        self.assertEqual(er, self._state_A.compute_battle_strength("poparea"))


    def test_merge_with(self):
        """Test merge_with() method."""

        new_state = copy.deepcopy(TEST_STATES_DICT["A"])
        er = State.State(new_state)
        er._pop += TEST_STATES_DICT["B"]["pop"]
        er._area += TEST_STATES_DICT["B"]["area"]
        er._neighbors = []

        self._state_A.merge_with(self._state_B)

        attribute_keys = ("_pop", "_area", "_neighbors", "_growth_rate", "_name", "_id")
        for ak in attribute_keys:
            self.assertEqual(getattr(er, ak), getattr(self._state_A, ak))


    def test_clean_neighborhood(self):
        """Test clean_neighborhood() method."""

        invalid_neighbors = ["A",]
        er = []
        state = State.State(copy.deepcopy(TEST_STATES_DICT["B"]))
        state.clean_neighborhood(invalid_neighbors)

        self.assertEqual(er, state.get_neighbors())


    def test_get_name(self):
        """Test get_name() method."""

        er = TEST_STATES_DICT["A"]["name"]
        self.assertEqual(er, self._state_A.get_name())


    def test_get_population(self):
        """Test get_population() method."""

        er = TEST_STATES_DICT["B"]["pop"]
        self.assertEqual(er, self._state_B.get_population())


    def test_get_area(self):
        """Test get_area() method."""

        er = TEST_STATES_DICT["B"]["area"]
        self.assertEqual(er, self._state_B.get_area())


    def test_get_history(self):
        """Test get_history() method."""

        er = {"pop": [TEST_STATES_DICT["A"]["pop"]]}
        self.assertEqual(er, self._state_A.get_history())


    def test_get_neighbors(self):
        """Test get_neighbors() method."""

        er = TEST_STATES_DICT["A"]["neighbors"]
        self.assertEqual(er, self._state_A.get_neighbors())


    def test_add_neighbor(self):
        """Test add_neighbor() method."""

        new_neighbor = "C"
        er = copy.deepcopy(TEST_STATES_DICT["A"]["neighbors"])
        er.append(new_neighbor)
        er = list(set(er))

        state = State.State(copy.deepcopy(TEST_STATES_DICT["A"]))
        state.add_neighbor(new_neighbor)
        self.assertEqual(er, state.get_neighbors())
