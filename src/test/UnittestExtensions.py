#!/usr/bin/env python3
"""
    Unittest Extensions
    ===================

    Special function tests.

"""

import numpy as np
import unittest as ut



def assertDeepAlmostEqual(test_case, expected, actual, *args, **kwargs):
    """Almost-Equal Assert Method for Complex Data Structures

    Assert that two complex structures have almost equal contents. Compares, lists,
    dicts and tuples recursively. Checks numeric values usinf test_case's
    :py:meth:`unittest.TesstCase.assertAlmostEqual` and checks all other values
    with :py:meth:`unittest.TestCase.assertEqual`. Accepts additional positional
    and keyword arguments and passes those intact to assertAlmostEqual() (that's
    how you specify comparison precision).

    Source: https://github.com/larsbutler/og_engine/blob/master/test/utils/helpers.py
    """
    
    is_root = not "__trace" in kwargs
    trace = kwargs.pop("__trace", "ROOT")
    try:
        if isinstance(expected, (int, float, complex)):
            test_case.assertAlmostEqual(expected, actual, *args, **kwargs)

        elif isinstance(expected, (list, tuple, np.ndarray)):
            test_case.assertEqual(len(expected), len(actual))

            for index in range(len(expected)):
                v1, v2 = expected[index], actual[index]
                assertDeepAlmostEqual(test_case, v1, v2, __trace = repr(index), *args, **kwargs)

        elif isinstance(expected, dict):
            test_case.assertEqual(set(expected), set(actual))

            for key in expected:
                assertDeepAlmostEqual(test_case, expected[key], actual[key], __trace = repr(key), *args, **kwargs)

        else:
            test_case.assertEqual(expected, actual)

    except AssertionError as exc:
        exc.__dict__.setdefault("traces", []).append(trace)
        if is_root:
            trace = " -> ".join(reversed(exc.traces))
            exc = AssertionError("{:s}\nTRACE: {:s}".format(exc.args[0], trace))

        raise exc
