import os
import sys
import csv
import json
import collections


def relative_path(fn):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fn))


def csv_reader_converter(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'latin-1') for cell in row]


def load_csv_columns(filename, column_names=None, delimiter=','):
    r = []
    with open(filename, 'r') as f:
        data_file = csv_reader_converter(f, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        headers = next(data_file, None)  # parse the headers
        columns = {}
        for (i, h) in enumerate(headers):
            h = h.strip()
            if h in column_names or not column_names:
                columns[i] = h

        for line in data_file:
            d = {}
            for (column, index) in columns.items():
                rename = column_names[index]
                value = line[column].strip()
                d[rename] = value
            r.append(d)
        return r


def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))


def split_dict_by(data, key, subkey=None):
    split_dict = collections.defaultdict(list)
    for item in data:
        if subkey:
            try:
                key_val = item[key][subkey]
            except KeyError:
                print 'unable to find [%s][%s] in item %s' % (key, subkey, item['id'])
                continue
        else:
            try:
                key_val = item[key]
            except KeyError:
                print "unable to find [%s] in item %s" % (key, item['id'])
                continue
        split_dict[key_val].append(item)
    return split_dict


def read_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def write_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))
