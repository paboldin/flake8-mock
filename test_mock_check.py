
import unittest
import ast

import mock_check

simplest = """
@mock.patch("a")
def test_abc(mock_a):
    pass
"""

full = """
def b():
    pass

@b()
@mock.patch("aaa.b")
@mock.patch("a", f=10)
@b
def test_abc(mock_a, mock__b):
    pass
"""

missing = """
@mock.patch("a")
def test_abc():
    pass
"""

prefixed = """
@mock.patch("a.b.c.d.e.f.bb_very_long_line")
def test_abc(mock_bb_very):
    pass
"""


class MockCheckerTestCase(unittest.TestCase):

    def mock_check(self, text):
        return [l[2] for l in mock_check.MockChecker(ast.parse(text)).run()]

    def test_simplest(self):
        errors = self.mock_check(simplest)
        self.assertEqual([], errors)

    def test_prefixed(self):
        errors = self.mock_check(prefixed)
        self.assertEqual([], errors)

    def test_missing(self):
        errors = self.mock_check(missing)
        self.assertEqual(
            ["C902 Invalid mocks and/or args (args: [], mocks: ['a'])"],
            errors)

    def test_full(self):
        errors = self.mock_check(full)
        self.assertEqual(
            ["C902 Invalid mocks and/or args (args: ['a', '_b'], "
             "mocks: ['a', 'b'])"],
            errors)

if __name__ == "__main__":
    unittest.main()
