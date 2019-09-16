import csv
from datetime import datetime
from datetime import timedelta

with open('values.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    csv_list = list(csv_reader)

    bg_data = []
    bg_labels = []

    """ We have to got bottom to top to make it chronological """
    row = int(len(csv_list) / 5)
    while row > 18:
        if csv_list[row][5] != 'cbg':
            row -= 1
        else:
            good_bgs = []
            for test_index in range(row, row-12, -1):
                previousTime = datetime.strptime(csv_list[row+1][0], '%Y-%m-%dT%H:%M:%S')
                this_time = datetime.strptime(csv_list[row][0], '%Y-%m-%dT%H:%M:%S')
                time_delta = this_time - previousTime
                if time_delta.seconds > 310 or len(csv_list[test_index][8]) < 3:
                    row = test_index
                    break
                else:
                    good_bgs.append(float(csv_list[test_index][8]) * 16.67)
            if len(good_bgs) == 12:
                next_time_index = row - 18
                next_time = datetime.strptime(csv_list[next_time_index][0], '%Y-%m-%dT%H:%M:%S')
                this_time = datetime.strptime(csv_list[row][0], '%Y-%m-%dT%H:%M:%S')
                time_delta = next_time - this_time
                if 5300 < time_delta.seconds < 5500 and len(csv_list[next_time_index][8]) > 3:
                    bg_data.append(good_bgs)
                    if float(csv_list[next_time_index][8]) * 16.67 < 80:
                        bg_labels.append(0)
                    elif float(csv_list[next_time_index][8]) * 16.67 < 180:
                        bg_labels.append(1)
                    else:
                        bg_labels.append(2)
            row -= 1

    print(bg_data)
    print(bg_labels)
