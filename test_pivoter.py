from unittest import TestCase

from pivoter import *

def extract(fname):
    input = read_csv(fname)
    return list(pivot(input))

def read_csv(fname):
    import csv
    with open(fname) as finput:
        return list(csv.DictReader(finput))

class TestPivoter(TestCase):

    def test_cli(self):
        parse_cli(["samples/sample_ABC.csv"])

    def test_main(self):
        main(parse_cli(["samples/sample_ABC.csv"]))

    def test_pivoter(self):
        result = extract("samples/sample_ABC.csv")
        expected = read_csv("samples/result_ABCD.csv")
        self.assertItemsEqual(result, expected)


class TestColumnDescriptor(TestCase):

    descriptor_row = ("account","Jan-09","Feb-09","Mar-09","Apr-09","May-09","Jun-09","Jul-09","Aug-09","Sep-09","Oct-09","Nov-09","Dec-09")

    def test_first_col(self):
        input = parse_column_descriptors(self.descriptor_row)
        self.assertEqual(input[0], "account")

    def test_row_date(self):
        input = parse_column_descriptors(self.descriptor_row)
        self.assertEqual(input[1], "2009-01")

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