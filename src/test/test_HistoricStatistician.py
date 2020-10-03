#!/usr/bin/env python3
"""
    Testing HistoricStatistician Module
    ===================================

    Each and every method must have its designated test.

"""

import sys
import numpy as np
import unittest as ut

sys.path.append("../")

import HistoricStatistician as hs


TEST_HISTORY = {
    'year': [2020, 2021, 2022, 2023],
    'states': [['A', 'B', 'C', 'D'], ['B', 'C', 'D'], ['B', 'C'], ['C']],
    'n_of_states': [4, 3, 2, 1],
    'world_population': [75000, 70145, 55884, 38549],
    'n_of_battles': [0, 1, 1, 1],
    'n_of_fatalities': [0, 5555, 14161, 17335],
    'n_of_pop_increse': [0, 700, -100, 0]
}



class test_HistoricStatistician(ut.TestCase):
    def setUp(self):
        self._hs = hs.HistStat(TEST_HISTORY)


    @ut.skip("Skipping since only calling other methods - no added functionality")
    def test_run(self):
        """Test run() method."""

        pass


    def test_extract_summary(self):
        """Test extract_summary() method."""

        cr = self._hs.extract_summary()
        er = {'end_population': 38549,
            'end_states': ['C'],
            'end_states_n': 1,
            'end_year': 2023,
            'history_duration': 4,
            'netto_delta_pop': -36451,
            'start_population': 75000,
            'start_states': ['A', 'B', 'C', 'D'],
            'start_states_n': 4
        }

        self.assertEqual(cr, er)


    def test_compute_battle_statistics(self):
        """Test compute_battle_statistics() method."""

        cr = self._hs.compute_battle_statistics()
        er = {'fatalities': {'avg': 12350.33,
            'max': 17335,
            'max_year': 2023,
            'total': 37051},
            'n_of_battles': [1, 1, 1],
            'n_of_fatalities': [5555, 14161, 17335],
            'tot_battles': 3
        }

        self.assertEqual(cr, er)


    @ut.skip("Skipping as long as GUI test framework not setup")
    def test_plot_world_population(self):
        """Test plot_world_population."""

        NotImplemented


    @ut.skip("Skipping as non-funcitonal")
    def test_print_results(self):
        """Test print_world_population."""

        pass
