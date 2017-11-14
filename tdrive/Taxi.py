import os
from datetime import datetime
from time import mktime


class Taxi:
    def __init__(self, file_path):
        ''' Constructor for Taxi class. '''
        if not os.path.exists(file_path):
            print('Error: ' + file_path + ' does not exist')
            self = None
        else:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            data_len = len(lines)
            self.ts = [0] * data_len
            self.lat = [0.0]*data_len
            self.lon = [0.0]*data_len
            self.data_len = data_len
            i = 0
            for line in lines:
                xs = line.strip().split(',')
                self.id = int(xs[0])
                date_str, time_str = xs[1].split()
                year, month, day = [int(x) for x in date_str.split('-')]
                hour, min, sec = [int(x) for x in time_str.split(':')]
                dt = datetime(year, month, day, hour, min, sec)
                self.ts[i] = mktime(dt.timetuple())

                self.lat[i] = float(xs[2])
                self.lon[i] = float(xs[3])
                i += 1


def load_taxis(dir_path, max_num_taxis=None):
    taxis = []
    if not os.path.exists(dir_path):
        print('Error: ' + dir_path + ' does not exist')
    elif not os.path.isdir(dir_path):
        print('Error: ' + dir_path + ' is not a directory')
    else:
        taxi_ids = []
        for fname in os.listdir(dir_path):
            file_path = os.path.join(dir_path, fname)
            name, ext = os.path.splitext(fname)
            if os.path.isfile(file_path) and '.txt':
                try:
                    stat = os.stat(file_path)
                    if stat.st_size:
                        taxi_ids.append(int(name))
                except:
                    pass
        taxi_ids.sort()
        if max_num_taxis:
            taxi_ids = taxi_ids[:max_num_taxis]
        print('Loading ' + str(len(taxi_ids)) + ' taxis...')
        for id in taxi_ids:
            file_path = os.path.join(dir_path, str(id) + '.txt')
            taxis.append(Taxi(file_path))
            if 0 == len(taxis) %  1000:
                print('  ' + str(len(taxis)))
        print('Done.')
    return taxis
