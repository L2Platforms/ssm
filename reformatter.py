import argparse
import csv
import datetime
import sys
import time

from math import sin, cos, sqrt, atan2, radians


class Reformatter(object):
    def __init__(self, in_file, start=0, gap='7d'):
        self.data = None
        self.data_dict = {}
        self.final_table = []
        self.formatted_table = {}
        self.gap = gap
        self.in_file = in_file
        self.out_file = self.in_file.replace('.csv', '_formatted.txt')
        self.quality = ['1', '2', '3', 'A', 'B']
        self.radius = 6378100
        self.start = start
        self.table_header = ['"id"', '"date"', '"lc"', '"lon"', '"lat"']

        self.gap_to_time()
        self.read_data()
        self.remove_quality_and_time()
        self.remove_duplicates()
        self.remove_high_speed()

    def remove_quality_and_time(self):

        for i, row in reversed(list(enumerate(self.data))):
            if i == 0 or not row:
                continue

            ts = self.convert_dt_to_ts(row[3])

            if row[5] not in self.quality or ts < self.start:
                del (self.data[i])

    def remove_duplicates(self):
        for i, row in enumerate(self.data):
            if i == 0 or not row:
                continue
            if row[1] not in self.data_dict:
                self.data_dict[row[1]] = []
            if self.data[i - 1] and self.data[i][3] == self.data[i - 1][3]:
                if self.data_dict[row[1]] and self.data_dict[row[1]][-1][3] == self.data[i][3]:
                    del (self.data_dict[row[1]][-1])
                continue

            self.data_dict[row[1]].append(row)

    def remove_high_speed(self):

        for iD in self.data_dict:
            for i, _ in reversed(list(enumerate(self.data_dict[iD]))):
                if i == 0:
                    continue
                lat1 = eval(self.data_dict[iD][i - 1][6])
                lat2 = eval(self.data_dict[iD][i][6])
                lon1 = eval(self.data_dict[iD][i - 1][7])
                lon2 = eval(self.data_dict[iD][i][7])
                time1 = self.convert_dt_to_ts(self.data_dict[iD][i - 1][3])
                time2 = self.convert_dt_to_ts(self.data_dict[iD][i][3])
                speed = self.calculate_speed(lat1, lon1, lat2, lon2, time1, time2)
                if speed > 2:
                    del (self.data_dict[iD][i])

    def calculate_speed(self, lat1, lon1, lat2, lon2, time1, time2):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.radius * c
        speed = distance / (time2 - time1)

        return speed

    def gap_to_time(self):
        length = self.gap[:-1]
        time_unit = self.gap[-1].lower()
        if time_unit.endswith('d'):
            self.gap = eval(length) * 24 * 3600
        elif time_unit.endswith('h'):
            self.gap = eval(length) * 3600

    def read_data(self):
        kwargs = {'newline': ''}
        mode = 'r'
        if sys.version_info < (3, 0):
            kwargs.pop('newline', None)
            mode = 'rb'
        with open(self.in_file, mode, **kwargs) as cFile:
            reader = csv.reader(cFile, delimiter=',', quotechar='"')
            self.data = [row for row in reader]

    @staticmethod
    def convert_dt_to_ts(dt):
        ts = time.mktime(datetime.datetime.strptime(dt, "%H:%M:%S %d-%b-%Y").timetuple())
        return ts

    def format_data(self):

        # table_header = ['"id"', 'date', '"lc"', '"lon"', '"lat"']

        for iD in self.data_dict:
            if iD not in self.formatted_table:
                self.formatted_table[iD] = []
                # self.formatted_table[iD].append(table_header)
            for row in self.data_dict[iD]:
                ts = self.convert_dt_to_ts(row[3])

                if ts > self.start and row[5] in self.quality:
                    id_str = str(row[1])
                    date = row[3]
                    lc = str(row[5])
                    lon = row[7]
                    lat = row[6]

                    formatted_row = [id_str, date, lc, lon, lat]
                    self.formatted_table[iD].append(formatted_row)

    def create_tracks(self):
        quotechar = '"'

        self.final_table.append(self.table_header)
        last_time = None
        for key in self.formatted_table:
            track = []
            track_num = 1
            for i, line in enumerate(self.formatted_table[key]):
                line.append(self.convert_dt_to_ts(line[1]))
                if i == 0:
                    line[0] = quotechar + line[0] + '.' + str(track_num) + quotechar
                else:
                    if (line[-1] - last_time) >= 1209600:

                        if len(track) > 20 and (track[-1][-1] - track[0][-1]) >= 18 * 3600:
                            track_num += 1
                            for tLine in track:
                                self.final_table.append(tLine[:-1])
                        track = []
                    line[0] = quotechar + line[0] + '.' + str(track_num) + quotechar

                line[2] = quotechar + line[2] + quotechar

                last_time = line[-1]

                readable = datetime.datetime.fromtimestamp(self.convert_dt_to_ts(line[1])).isoformat()
                line[1] = readable.replace('T', ' ')

                track.append(line)

    def save_data(self):

        kwargs = {'newline': ''}
        mode = 'w'
        if sys.version_info < (3, 0):
            kwargs.pop('newline', None)
            mode = 'wb'

        with open(self.out_file, mode, **kwargs) as cFile:
            for line in self.final_table:
                for item in line[:-1]:
                    cFile.write(str(item) + ',')

                cFile.write(str(line[-1]) + '\n')
            # writer = csv.writer(cFile, delimiter=',')
            # writer.writerows(self.final_table)


def main():
    desc = 'This code is designed to format data extracted from Wildlife Computers Portal'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--file', '-f', default=None, help='Must be a .csv file')
    parser.add_argument('--start_date', '-a', default=0, help='Start Datetime of tag (YYYY-MM-DDThh:mm:ss)')
    parser.add_argument('--gap', '-g', default='7d',
                        help='Defines the acceptable gap between tracks in days or hours (e.g., 7d or '
                             '72h, etc)')

    args = parser.parse_args()

    if not args.file.endswith('.csv'):
        raise ValueError('Invalid File Type!!! Please input .csv file')

    ref = Reformatter(in_file=args.file, start=args.start_date, gap=args.gap)
    ref.format_data()
    ref.create_tracks()
    ref.save_data()


if __name__ == "__main__":
    main()
