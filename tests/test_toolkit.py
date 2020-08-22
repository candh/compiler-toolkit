import unittest
from toolkit.modules.elim_left_recursion import elim_lr
from toolkit.modules.elim_null import elim_null
from toolkit.modules.is_nullable import is_nullable
from toolkit.modules.elim_unit import elim_unit, remove_same_rules
from toolkit.modules.make_first_sets import first_sets
from toolkit.modules.make_follow_sets import follow_sets
from toolkit.modules import grammar as gm
from .fixtures import cases


class CompilerToolKitTestCase(unittest.TestCase):
    def test_parse_grammar(self):
        for x, y in zip(cases.parser_test_cases, cases.parser_test_cases_targets):
            self.assertEqual(gm.parse(x), y)

    def test_elim_left_recursion(self):
        for x, y in zip(cases.elim_lr_test_cases, cases.elim_lr_test_cases_targets):
            x, f = x
            x = gm.parse(x)
            if f:
                x = gm.reverse_grammar(x)
            y = gm.parse(y)
            ng = elim_lr(x)
            self.assertEqual(ng, y)

    def test_elim_null_prod(self):
        for x, y in zip(cases.elim_null_test_cases, cases.elim_null_test_cases_targets):
            x = gm.parse(x)
            y = gm.parse(y)
            ng = elim_null(x)
            self.assertEqual(ng, y)

    def test_elim_unit_prod(self):
        for x, y in zip(cases.elim_unit_test_cases, cases.elim_unit_test_cases_targets):
            x = gm.parse(x)
            y = gm.parse(y)
            ng = elim_unit(x)
            ng = remove_same_rules(ng, False, False)
            self.assertEqual(ng, y)

    def test_is_nullable(self):
        for x, y in zip(
            cases.is_nullable_test_cases, cases.is_nullable_test_cases_targets
        ):
            x = gm.parse(x)
            self.assertEqual(is_nullable("S", x), y)

    def test_first_set(self):
        for x, y in zip(
            cases.first_follow_set_test_cases, cases.first_set_test_cases_targets
        ):
            x = gm.parse(x)
            fs = first_sets(x)
            self.assertEqual(fs, y)

    def test_follow_set(self):
        for x, y in zip(
            cases.first_follow_set_test_cases, cases.follow_set_test_cases_targets
        ):
            x = gm.parse(x)
            fs = first_sets(x)
            start = list(x.keys())[0]
            fls = follow_sets(start, x, fs)
            self.assertEqual(fls, y)


if __name__ == "__main__":
    unittest.main()
