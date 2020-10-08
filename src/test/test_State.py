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
        self._state_A = State.State(TEST_STATES_DICT["A"])
        self._state_B = State.State(TEST_STATES_DICT["B"])


    def test_State_constructor(self):
        """Test state constructor."""

        exception_keys = ("_pretty_name", "_history")

        for kk, vv in self._state_A.__dict__.items():
            if kk not in exception_keys:
                self.assertEqual(TEST_STATES_DICT["A"][kk[1:]], vv)


    def test_update_history(self):
        """Test update_history() method."""
        NotImplemented


    def test_grow(self):
        """Test grow() method."""
        NotImplemented


    def test_compute_population_growth_delta(self):
        """Test test_compute_population_growth_delta() method."""
        NotImplemented


    def test_update_populations_after_battle(self):
        """Test update_population_after_battle() method."""
        NotImplemented


    def test_compute_battle_strength(self):
        """Test compute_battle_strength() method."""
        NotImplemented


    def test_merge_with(self):
        """Test merge_with() method."""
        NotImplemented


    def test_clean_neighborhood(self):
        """Test clean_neighborhood() method."""
        NotImplemented


    def test_get_name(self):
        """Test get_name() method."""
        NotImplemented


    def test_get_population(self):
        """Test get_population() method."""
        NotImplemented


    def test_get_area(self):
        """Test get_area() method."""
        NotImplemented


    def test_get_neighbors(self):
        """Test get_neighbors() method."""
        NotImplemented


    def test_add_neighbor(self):
        """Test add_neighbor() method."""
        NotImplemented
