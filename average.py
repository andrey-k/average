# -*- coding: utf-8 -*-
import csv
import sys
import datetime
import argparse

def createParser():
    """Command line arguments parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-r', '--reverse', action='store_const',
                        const=True, default=False)
    parser.add_argument('-m', '--month', action='store_const',
                        const=True, default=False)

    return parser

data = {}
def getData(file_name, month):
    with open(file_name, 'rb') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=';')
        time_format = '%d.%m.%Y'
        for row in data_reader:
            date_data = row[0].split(' ')[0]
            if month:
                date_data = date_data.split('.')
                date_data = "{}.{}".format(date_data[1],date_data[2])
                time_format = '%m.%Y'
            date_data = datetime.datetime.strptime(date_data, time_format)
            if date_data in data.keys():
                if len(row[1]) > 0:
                    data[date_data].append(int(row[1]))
            else:
                if len(row[1]) > 0:
                    data[date_data] = [int(row[1])]
    print 'done'
    return data

def setData(file_name, data, reverse, month):
    with open(file_name, 'wb') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=';')
        time_format = '%d.%m.%Y'
        if month:
            time_format = '%m.%Y'

        if reverse:
            data_dict = reversed(sorted(data.iterkeys()))
        else:
            data_dict = sorted(data.iterkeys())
        for key in data_dict:
            row_data = [key.strftime(time_format)]
            average = sum(data[key])/float(len(data[key]))
            row_data.append(average)
            for v in data[key]:
                row_data.append(v)
            data_writer.writerow(row_data)

def main(namespace):
    if namespace.reverse:
         print 'start transformation. reverse mode'
    else:
        print 'start transformation'

    input_file =  "{}.csv".format(namespace.file)
    data = getData(input_file, namespace.month)
    print 'do calculations'
    output_file = "{}_result.csv".format(namespace.file)
    setData(output_file, data, namespace.reverse, namespace.month)
    print "done. result in {} file".format(output_file)

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    sys.exit(main(namespace))
