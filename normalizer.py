import csv
import sys
import datetime
import re

class Normalizer:
    def __init__(self):
        self.data = self.pull_data();

    #open file from name input in console and read to python list object
    def pull_data(self):
        csv_file = sys.stdin.readlines()
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

    #empit output to terminal        
    def emit(self, data):
        outputfile = sys.stdout
        fieldnames = self.data[0].keys()
        writer = csv.DictWriter(outputfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return True

    #convert timestamp to RCF3339 and from US/Pacific to US/Eastern time
    def time_to_east_rfc(self, timestamp):
        #pacific timezone offset
        pt = datetime.timezone(datetime.timedelta(hours=8))
        print(pt)
        #eastern timezone offset
        et = datetime.timedelta(hours=5)
        m, d, y, h, mi, s, am = re.split('[/:. ]', timestamp)
        return datetime.datetime(int(y), int(m), int(d), int(h), int(mi), int(s), tzinfo=pt).astimezone(tz=et).isoformat()

    #add 0 prefix to zip if less than 5 digits
    def normalize_zip(self, zip):
        return zip if len(zip) == 5 else '0' + zip

    #split 'HH:MM:SS.MS' into datetime components to create timedelta object and return total_seconds from object
    def convert_duration(self, duration):
        h, m, s, ms = re.split('[:. ]', duration)
        t = datetime.timedelta(seconds=int(s), milliseconds=int(ms), minutes=int(m), hours=int(h))
        return t.total_seconds()

    def normalize_csv(self):
        for line in self.data:
            line['Timestamp'] = self.time_to_east_rfc(line['Timestamp'])
            line['ZIP'] = self.normalize_zip(line['ZIP'])
            line['FullName'] = line['FullName'].upper()
            line['FooDuration'] = self.convert_duration(line['FooDuration'])
            line['BarDuration'] = self.convert_duration(line['BarDuration'])
            line['TotalDuration'] = line['FooDuration'] + line['BarDuration']

        self.emit(self.data)

if __name__ == "__main__":
    rate_finder = Normalizer()
    rate_finder.normalize_csv()
