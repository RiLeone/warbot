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


class test_warbot(ut.TestCase):
    def setUp(self):
        pass


    def test_load_players(self):
        """Test load_players() method"""

        filename = "test_data.json"
        wb = warbot.WarBot(filename)
        cr = wb.load_players(filename) # In a way redundant, but this is what we actually wanna test here.
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
