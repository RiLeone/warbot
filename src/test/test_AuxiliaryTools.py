#!/usr/bin/env python3
"""
    Testing AuxiliaryTools Module
    =============================

    Each and every method must have its designated test.

"""

import sys
import copy
import logging
import unittest as ut

sys.path.append("../")

import AuxiliaryTools



class test_AuxiliaryTools(ut.TestCase):
    def setUp(self):
        pass


    @ut.skip("Not sure how to test this")
    def test_setup_logging(self):
        """Test setup_logging() function"""

        NotImplemented


    @ut.skip("Not truely functional")
    def test_setup_matplotlib_options(self):
        """Test setup_matplotlib_options() function"""

        pass


    def test_parse_argvs(self):
        """Test parse_argvs() function"""

        subtests = []
        original_argv = [__file__, ]
        subtests.append({"argvs": None,
            "er": AuxiliaryTools.DEFAULT_MAIN_OPTS,
            "msg": "No argvs"
            }
        )

        valid_v_opt = copy.deepcopy(AuxiliaryTools.DEFAULT_MAIN_OPTS)
        valid_v_opt["WarBot.run"]["verbose"] = True
        subtests.append({"argvs": ["-v"],
            "er": valid_v_opt,
            "msg": "Valid -v option"
            }
        )

        subtests.append({"argvs": ["invalid", "options"],
            "er": AuxiliaryTools.DEFAULT_MAIN_OPTS,
            "msg": "Invalid option(s)"
            }
        )

        for ii, sbt in enumerate(subtests):
            with self.subTest(i = ii, msg = sbt["msg"]):
                if sbt["argvs"] is not None:
                    sys.argv = original_argv.copy() + sbt["argvs"]

                else:
                    sys.argv = original_argv.copy()

                cr = AuxiliaryTools.parse_args()
                self.assertEqual(sbt["er"], cr)
