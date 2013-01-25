
def main(params):
    import csv
    # Goal
    # For each row
    #   where label is first column
    #   produce one row with a label and an index into a hashed set of labels
    #   save the file to git
    with open(params.file) as finput:
        input = csv.DictReader(finput)
        pivot(input)

def pivot(table, seed=set()):
    result = []
    for row in table:
        pass
    return result

def parse_column_descriptors(row):
    label = row[0]
    str_cols = row[1:]
    date_cols = [parse_date_time(col) for col in str_cols]
    formatted_cols = [format_date_time(col) for col in date_cols]
    return [label] + formatted_cols

def format_date_time((month, year)):
    return '%4d-%02d' % (year, month)

def parse_date_time(date_time):
    monthNameToInt = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    month_name, years = date_time.split("-")
    month, year = monthNameToInt[month_name], int(years) + 2000
    return month, year

def parse_cli(args):
    import argparse
    parser = argparse.ArgumentParser("pivoter")
    parser.add_argument("file", help="")
    return parser.parse_args(args)


if __name__ == '__main__':
    import sys
    params = parse_cli(sys.argv[1:])
    main(params)