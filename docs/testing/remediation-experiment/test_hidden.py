"""Hidden acceptance tests for the csvexport brief. Never shown to trial agents."""
import datetime as dt
import decimal
import io
import math
import unittest

import csvexport


def ex(rows, columns, **kw):
    return csvexport.export(rows, columns, **kw)


class Format(unittest.TestCase):
    def test_header_only_when_no_rows(self):
        self.assertEqual(ex([], ["a", ("b", "B")]), "a,B\r\n")

    def test_crlf_after_last_record(self):
        self.assertEqual(ex([{"a": 1}], ["a"]), "a\r\n1\r\n")

    def test_column_order_and_header_tuple(self):
        self.assertEqual(ex([{"a": 1, "b": 2}], [("b", "Bee"), "a"]), "Bee,a\r\n2,1\r\n")

    def test_missing_and_none_empty(self):
        self.assertEqual(ex([{"a": None}], ["a", "b"]), "a,b\r\n,\r\n")

    def test_quote_comma(self):
        self.assertEqual(ex([{"a": "x,y"}], ["a"]), 'a\r\n"x,y"\r\n')

    def test_quote_doubled(self):
        self.assertEqual(ex([{"a": 'say "hi"'}], ["a"]), 'a\r\n"say ""hi"""\r\n')

    def test_quote_embedded_newline_lf(self):
        self.assertEqual(ex([{"a": "l1\nl2"}], ["a"]), 'a\r\n"l1\nl2"\r\n')

    def test_quote_embedded_cr(self):
        self.assertEqual(ex([{"a": "l1\rl2"}], ["a"]), 'a\r\n"l1\rl2"\r\n')

    def test_header_quoted_when_needed(self):
        self.assertEqual(ex([], [("a", "x,y")]), '"x,y"\r\n')

    def test_bom(self):
        self.assertEqual(ex([], ["a"], bom=True), "\ufeffa\r\n")

    def test_no_bom_default(self):
        self.assertFalse(ex([], ["a"]).startswith("\ufeff"))


class Values(unittest.TestCase):
    def test_bool_before_int(self):
        self.assertEqual(ex([{"a": True, "b": False}], ["a", "b"]), "a,b\r\ntrue,false\r\n")

    def test_int_negative_not_prefixed(self):
        self.assertEqual(ex([{"a": -5}], ["a"]), "a\r\n-5\r\n")

    def test_float_repr(self):
        self.assertEqual(ex([{"a": 0.1}], ["a"]), "a\r\n0.1\r\n")

    def test_float_negative_not_prefixed(self):
        self.assertEqual(ex([{"a": -1.5}], ["a"]), "a\r\n-1.5\r\n")

    def test_nan_raises_with_key_and_index(self):
        rows = [{"amount": 1.0}, {"amount": 2.0, "skip": 1}, {"amount": math.nan}]
        with self.assertRaises(ValueError) as cm:
            ex(rows, ["amount"], filters={"amount": ("range", None, None)})
        msg = str(cm.exception)
        self.assertIn("amount", msg)
        self.assertIn("2", msg)

    def test_nan_index_counts_exported_rows_only(self):
        rows = [{"k": 0, "a": 1.0}, {"k": 1, "a": 1.0}, {"k": 1, "a": math.inf}]
        with self.assertRaises(ValueError) as cm:
            ex(rows, ["a"], filters={"k": 1})
        self.assertRegex(str(cm.exception), r"\b1\b")
        self.assertNotRegex(str(cm.exception), r"\b2\b")

    def test_inf_raises(self):
        with self.assertRaises(ValueError):
            ex([{"a": -math.inf}], ["a"])

    def test_decimal(self):
        self.assertEqual(ex([{"a": decimal.Decimal("1.10")}], ["a"]), "a\r\n1.10\r\n")

    def test_date(self):
        self.assertEqual(ex([{"a": dt.date(2026, 1, 2)}], ["a"]), "a\r\n2026-01-02\r\n")

    def test_aware_datetime_to_utc_no_micros(self):
        tz = dt.timezone(dt.timedelta(hours=-5))
        v = dt.datetime(2026, 1, 2, 23, 30, 15, 999999, tzinfo=tz)
        self.assertEqual(ex([{"a": v}], ["a"]), "a\r\n2026-01-03T04:30:15Z\r\n")

    def test_naive_datetime_raises_naming_key(self):
        with self.assertRaises(ValueError) as cm:
            ex([{"when": dt.datetime(2026, 1, 1)}], ["when"])
        self.assertIn("when", str(cm.exception))

    def test_unsupported_type_raises_naming_key(self):
        with self.assertRaises(TypeError) as cm:
            ex([{"blob": b"x"}], ["blob"])
        self.assertIn("blob", str(cm.exception))


class Injection(unittest.TestCase):
    def test_prefixes(self):
        for ch in ["=", "+", "-", "@", "\t", "\r"]:
            out = ex([{"a": ch + "1"}], ["a"])
            body = out.split("\r\n", 1)[1]
            self.assertTrue(body.lstrip('"').startswith("'" + ch), (ch, out))

    def test_prefix_then_quote(self):
        self.assertEqual(ex([{"a": "=1,2"}], ["a"]), "a\r\n\"'=1,2\"\r\n")

    def test_cr_prefixed_and_quoted(self):
        self.assertEqual(ex([{"a": "\rx"}], ["a"]), "a\r\n\"'\rx\"\r\n")

    def test_header_not_prefixed(self):
        self.assertEqual(ex([], [("a", "=h")]), "=h\r\n")

    def test_plain_string_untouched(self):
        self.assertEqual(ex([{"a": "a=b"}], ["a"]), "a\r\na=b\r\n")


class Filters(unittest.TestCase):
    ROWS = [{"n": 1}, {"n": 2}, {"n": 3}, {"m": 9}, {"n": None}]

    def test_equality(self):
        self.assertEqual(ex(self.ROWS, ["n"], filters={"n": 2}), "n\r\n2\r\n")

    def test_range_inclusive_lo_exclusive_hi(self):
        self.assertEqual(ex(self.ROWS, ["n"], filters={"n": ("range", 1, 3)}), "n\r\n1\r\n2\r\n")

    def test_range_unbounded(self):
        self.assertEqual(ex(self.ROWS, ["n"], filters={"n": ("range", 2, None)}), "n\r\n2\r\n3\r\n")

    def test_missing_or_none_excluded(self):
        self.assertEqual(ex(self.ROWS, ["n"], filters={"n": ("range", None, None)}), "n\r\n1\r\n2\r\n3\r\n")

    def test_multiple_filters_all_must_hold(self):
        rows = [{"a": 1, "b": 1}, {"a": 1, "b": 2}]
        self.assertEqual(ex(rows, ["b"], filters={"a": 1, "b": 2}), "b\r\n2\r\n")

    def test_no_filters_keeps_rows_missing_keys(self):
        self.assertEqual(ex([{"m": 1}], ["n"]), 'n\r\n""\r\n')


class Streaming(unittest.TestCase):
    def test_stream_returns_none_and_writes(self):
        buf = io.StringIO()
        self.assertIsNone(ex([{"a": 1}], ["a"], stream=buf, bom=True))
        self.assertEqual(buf.getvalue(), "\ufeffa\r\n1\r\n")

    def test_generator_consumed_lazily(self):
        seen = []

        class Probe(io.StringIO):
            def write(self, s):
                seen.append(("w", len(s)))
                return super().write(s)

        def gen():
            for i in range(3):
                seen.append(("r", i))
                yield {"a": i}

        ex(gen(), ["a"], stream=Probe())
        first_r1 = seen.index(("r", 1))
        self.assertTrue(any(k == "w" for k, _ in seen[:first_r1]), seen)

    def test_one_shot_generator_returns_string(self):
        self.assertEqual(ex(({"a": i} for i in range(2)), ["a"]), "a\r\n0\r\n1\r\n")


class Surface(unittest.TestCase):
    def test_public_names(self):
        public = [n for n in dir(csvexport) if not n.startswith("_")]
        imported_modules = {n for n in public if type(getattr(csvexport, n)).__name__ == "module"}
        self.assertEqual(sorted(set(public) - imported_modules), ["export"])


if __name__ == "__main__":
    unittest.main()
