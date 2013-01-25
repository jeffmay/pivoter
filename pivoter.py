import sys

def main(params):
    import csv
    # Goal
    # For each row
    #   where label is first column
    #   produce one row with a label and an index into a hashed set of labels
    #   save the file to git
    table = read_table(params.input)
    result = pivot(table)
    result_table = convert_to_table(result)
    if params.output is not None:
        with open(params.output, "w") as output:
            dump_table(result_table, output)
    else:
        dump_table(result_table, sys.stdout)

def read_table(fname):
    import csv
    with open(fname) as finput:
        reader = csv.reader(finput)
        table = [tuple([c.strip() for c in row]) for row in reader]
    return table


def pivot(table, seed={}, start_index=1):
    _, month_dates = parse_header(table[0])
    rotated = rotate(table[1:])
    # get the accounts from all the first cols
    accounts = [account for account in rotated[0]]
    num_accounts = len(accounts)
    month_data = rotated[1:]
#    print rotated
    for i, data in enumerate(month_data):
        last_index = i + start_index
        month = format_date_time(month_dates[i])
        account = accounts[i % num_accounts]  # months rotate over accounts
        time_periods = data[1:]
        key = (account, month)
        entry = seed[key] if account in seed else Entry(last_index, month)
        for value in time_periods:
            entry.total += int(value)
        seed[key] = entry
    return seed

def convert_to_table(data):
    data = sorted(data.values())
    rows = [tuple([entry.account_id, entry.total, entry.month_date]) for entry in data]
    header = ("account", "total", "month_date")
    return [header] + rows

def dump_table(table, output):
    import csv
    writer = csv.writer(output)
    writer.writerows(table)


class Entry:
    def __init__(self, account_id, month_date, total=0):
        self.account_id = account_id
        self.month_date = month_date
        self.total = total

    def __eq__(self, other):
        return isinstance(other, Entry) and self.__dict__ == other.__dict__

    def __hash__(self):
        return sum((hash(item) for item in self.__dict__.items()))

    def __repr__(self):
        return "Entry(%s)" % ", ".join([str(self.account_id), str(self.total)])

    def __cmp__(self, other):
        diff_accounts = cmp(self.account_id, other.account_id)
        if diff_accounts:
            return diff_accounts
        else:
            return cmp(self.month_date, other.month_date)

def rotate(matrix):
    return zip(*matrix[:])

def parse_header(row):
    label = row[0]
    str_cols = row[1:]
    date_cols = [parse_date_time(col) for col in str_cols]
    return label, date_cols

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
    parser.add_argument("input", help="")
    parser.add_argument("-o", "--output", help="")
    return parser.parse_args(args)


if __name__ == '__main__':
    params = parse_cli(sys.argv[1:])
    main(params)