#!/usr/bin/env python3

import sys
import unittest
import solver


class solverTest( unittest.TestCase ) :

    def test_divide_list(self):
        self.assertEqual(solver.divide_list([8,2]), 4)
        self.assertEqual(solver.divide_list([16,4,4]), 1)
        self.assertEqual(solver.divide_list([1,2,80]), 0.00625)
        self.assertEqual(solver.divide_list([]), None)
        self.assertEqual(solver.divide_list([100, 10, 10, 1,1,1,1,1,1,1]) , 1)
        self.assertEqual(solver.divide_list([1,0]), None)
        self.assertEqual(solver.divide_list([0,1]), 0)

    def test_recurse(self):
        self.assertEqual(solver.recurse([8, [4,2]]), [8,2] )
        self.assertEqual(solver.recurse([[32,4], 2,1,1,1]), [8,2,1,1,1])
        self.assertEqual(solver.recurse([]), [])
        self.assertEqual(solver.recurse([[]]), [None])

    def test_solve(self):
        self.assertEqual(solver.solve([[16,[8,2],4],2,80]), 0.00625)
        self.assertEqual(solver.solve([4,1]), 4)
        self.assertEqual(solver.solve([0,1]), 0)
        self.assertEqual(solver.solve([1]), 1)
        self.assertEqual(solver.solve([]), None)

if __name__ == "__main__":
    unittest.main()

