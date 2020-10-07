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
    },
    "B": {
        "pop": 20000,
        "area": 1000,
        "id": 2,
        "neighbors": ["A"],
        "growth_rate": -0.01,
    }
}



class test_State(ut.TestCase):
    def setUp(self):
        pass

    
