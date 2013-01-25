from unittest import TestCase

from pivoter import *

def extract(fname):
    input = read_table(fname)
    return pivot(input)

class TestPivoter(TestCase):

    def test_cli(self):
        parse_cli(["samples/sample_ABC.csv"])

    def test_main(self):
        main(parse_cli(["samples/sample_ABC.csv"]))

    def test_pivoter(self):
        data = extract("samples/sample_ABC.csv")
        result_table = convert_to_table(data)
        expected_result = read_table("samples/result_ABCD.csv")
        print "actual: %s" % result_table
        print "expected: %s" % expected_result
        for actual, expected in result_table, expected_result:
            self.assertItemsEqual(actual, expected)

    def test_rotate(self):
        actual = rotate((("A","B","C"),(1, 2, 3)))
        expected = [("A", 1), ("B", 2), ("C", 3)]
        self.assertEqual(expected, actual)

    def test_convert_to_table(self):
        rows = convert_to_table({
            3: Entry(2, "2012-05"),
            1: Entry(1, "2012-03"),
            0: Entry(1, "2012-01"),
            2: Entry(2, "2012-03"),
            4: Entry(2, "2013-03"),
        })
        self.assertItemsEqual([
            Entry(1, "2012-01"),
            Entry(1, "2012-03"),
            Entry(2, "2012-03"),
            Entry(2, "2012-05"),
            Entry(2, "2013-03"),
        ], rows)



class TestColumnDescriptor(TestCase):

    descriptor_row = ("account","Jan-09","Feb-09","Mar-09","Apr-09","May-09","Jun-09","Jul-09","Aug-09","Sep-09","Oct-09","Nov-09","Dec-09")

    def test_first_col(self):
        account, _ = parse_header(self.descriptor_row)
        self.assertEqual(account, "account")

    def test_row_date(self):
        _, cols  = parse_header(self.descriptor_row)
        self.assertEqual(cols[0], (1, 2009))

class TestParseDateTime(TestCase):

    def test_splits_date(self):
        self.assertEqual(len(parse_date_time("Mar-12")), 2)

    def test_month_label(self):
        self.assertEqual(parse_date_time("Mar-12")[0], 3)

    def test_year_label(self):
        self.assertEqual(parse_date_time("Mar-12")[1], 2012)

class TestFormatDateTime(TestCase):

    def test_result(self):
        actual = format_date_time((03, 2011))
        self.assertEqual(actual, "2011-03")


if __name__ == "__main__":
    import unittest
    unittest.main()