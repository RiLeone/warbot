#!/usr/bin/env python3
"""
    Testing WorldSelector Module
    ============================

    Each and every method must have its designated test.

"""

import os
import sys
import unittest as ut

sys.path.append("../")

import WorldSelector


class test_WorldSelector(ut.TestCase):
    def setUp(self):
        self._root = os.path.dirname(__file__)


    def test_get_last_part_of_path(self):
        """Test get_last_part_of_path() function"""

        path = "I/am/fake"
        er = "fake"
        cr = WorldSelector.get_last_part_of_path(path)

        self.assertEqual(cr, er)


    @ut.skip("Skipping due to required user interaction")
    def test_select_world(self):
        """Test select_world() function"""

        pass


    def test_list_worlds(self):
        """Test list_worlds() function"""

        er = ["Testland", ]
        cr = WorldSelector.list_worlds(self._root)

        self.assertEqual(er, cr)


    def test_verify_choice(self):
        """Test verify choice() function"""

        dnames = WorldSelector.list_worlds(self._root)
        subtests = []

        subtests.append({"arg": -1,
                "er": self._root + "/worlds/Debugland/states.json",
                "msg": "Negative index"
            }
        )

        subtests.append({"arg": "Bla",
                "er": self._root + "/worlds/Debugland/states.json",
                "msg": "Invalid filename"
            }
        )

        subtests.append({"arg": "Testland",
                "er": self._root + "/worlds/Testland/states.json",
                "msg": "Valid string"
            }
        )

        subtests.append({"arg": 1,
                "er": self._root + "/worlds/Testland/states.json",
                "msg": "Valid index"
            }
        )

        for ii, sbt in enumerate(subtests):
            with self.subTest(i = ii, msg = sbt["msg"]):
                cr = WorldSelector.verify_choice(self._root, dnames, sbt["arg"])
                self.assertEqual(sbt["er"], cr)
