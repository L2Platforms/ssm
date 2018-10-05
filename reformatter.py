import argparse
import csv
import sys


class Reformatter(object):
    def __init__(self, in_file, start):
        self.data = None
        self.formatted_table = []
        self.in_file = in_file
        self.start = start
        self.quality = [1,2,3,'A','B']

    def read_data(self):
        kwargs = {'newline': ''}
        mode = 'r'
        if sys.version_info < (3, 0):
            kwargs.pop('newline', None)
            mode = 'rb'
        with open(self.in_file, mode, **kwargs) as cFile:
            reader = csv.reader(cFile, delimiter=',', quotechar='"')
            self.data = [row for row in reader]

    def format_data(self):
        quote='"'
        table_header = ['"id"', 'date', '"lc"', '"lon"', '"lat"']
        self.formatted_table.append(table_header)
        for row in self.data[1:]:
            if row[3] > self.start and row[5] in self.quality:
                id = quote + str(row[1]) + quote
#                 FIGURE OUT GOOD WAY TO FORMAT WITH QUOTES!!!!!!


def main():
    desc = 'This code is designed to format data extracted from Wildlife Computers Portal'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--file', '-f', default=None, help='Must be a .csv file')
    parser.add_argument('--start_date', '-a', default=None, help='Start Datetime of tag (YYYY-MM-DDThh:mm:ss)')

    args = parser.parse_args()

    if not args.file.endswith('.csv'):
        raise ValueError('Invalid File Type!!! Please input .csv file')

    ref = Reformatter(in_file=args.file)
    ref.read_data()

    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()
