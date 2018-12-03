import json
from datetime import datetime
from tqdm import tqdm


class Location:
    def __init__(self, data_path):
        with open(data_path, 'r') as file:
            self.data = json.load(file)['locations']

    def get_report(self, location, time, max_dist=0.1):
        max_distE7 = max_dist * 1e7
        latitude, longitude = location
        latitudeE7 = latitude * 1e7
        longitudeE7 = longitude * 1e7
        time_start, time_end = time
        timestamp_0 = time_start.timestamp() * 1000
        timestamp_1 = time_end.timestamp() * 1000

        weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        report = []
        report_weekdays = [0, 0, 0, 0, 0, 0, 0]

        for x in tqdm(self.data):
            distance2 = (x['latitudeE7'] - latitudeE7) ** 2 + (x['longitudeE7'] - longitudeE7) ** 2
            timestamp = float(x['timestampMs'])
            if distance2 < max_distE7 ** 2 and timestamp_0 < timestamp < timestamp_1:
                t = datetime.fromtimestamp(timestamp / 1000)
                t_string = t.strftime('%Y-%m-%d')
                report.append(t_string)

        report = list(set(report))  # remove duplicates
        report = sorted(report)

        for day_string in report:
            day = day_string.split('-')
            day = [int(d) for d in day]
            d = datetime(*day)
            weekday = d.weekday()
            report_weekdays[weekday] += 1
            print('{} \t {}'.format(day_string, weekday_list[weekday]))

        for day, count in zip(weekday_list, report_weekdays):
            print('{}: \t {}'.format(day, count))

        pass


if __name__ == '__main__':
    data_path = 'Takeout/Locatiegeschiedenis/Locatiegeschiedenis.json'
    location = Location(data_path)

    location.get_report((50.8, 4.7), (datetime(2018, 3, 12), datetime(2018, 12, 31)))
