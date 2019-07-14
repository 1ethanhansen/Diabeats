import csv
from datetime import datetime
from datetime import timedelta

with open('values.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    csv_list = list(csv_reader)

    jump_list = []

    row = 2
    while row < len(csv_list):
        if csv_list[row][5] != 'cbg':
            del(csv_list[row])
        else:
            previousTime = datetime.strptime(csv_list[row-1][0], '%Y-%m-%dT%H:%M:%S')
            this_time = datetime.strptime(csv_list[row][0], '%Y-%m-%dT%H:%M:%S')
            time_delta = previousTime - this_time

            previousValue = float(csv_list[row - 1][8]) * 18
            value = float(csv_list[row][8]) * 18
            delta = value - previousValue

            if time_delta.seconds > 310 and time_delta.seconds < 3600:
                num_missing_readings = (time_delta.seconds + 10) // 300
                print(num_missing_readings)
                missingDelta = delta / num_missing_readings
                print(missingDelta)
                for i in range(num_missing_readings):
                    missing_value = previousValue + (missingDelta * i)
                    missing_time = (previousTime + timedelta(seconds=300)).strftime('%Y-%m-%dT%H:%M:%S')
                    print(missing_value)
                    print(missing_time)
                    new_row = [missing_time, '', '', '', '', '', '', '', missing_value]
                    csv_list.insert(row, new_row)
                print("time jump @ {} seconds: {}".format(row, time_delta.seconds))

            twoPreviousValue = float(csv_list[row - 2][8]) * 18
            previousValue = float(csv_list[row - 1][8]) * 18
            previousDelta = previousValue - twoPreviousValue

            value = float(csv_list[row][8]) * 18
            delta = value - previousValue

            if delta > previousDelta+10 or delta < previousDelta-10:
                # print("row: {}  delta: {}  last delta: {}".format(row, delta, previousDelta))
                jump_list.append(row)
            row += 1

    index = 1
    good_runs = []
    while index < len(jump_list):
        if (jump_list[index] - jump_list[index - 1]) > 6:
            good_runs.append((jump_list[index - 1], jump_list[index]))
        index += 1
    print(len(jump_list))
    print(len(good_runs))
