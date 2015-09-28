import os, sys, csv, json, collections

# map colum names from gazetteer tsv to output json
COLUMNS = {
    'USPS': 'state',
    'GEOID': 'fips',
    'NAME': 'name',
    'INTPTLAT': 'lat',
    'INTPTLONG': 'lon',
}


# map state abbreviations to full name, for writing out
STATES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
    'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}


def relative_path(fn):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fn))


def converting_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'latin-1') for cell in row]


def load_gazetteer(filename):
    r = []
    with open(filename, 'r') as f:
        gazetteer = converting_csv_reader(f, delimiter="\t")
        headers = next(gazetteer, None)  # parse the headers
        columns = {}
        for (i, h) in enumerate(headers):
            h = h.strip()
            if h in COLUMNS:
                columns[i] = h

        for line in gazetteer:
            d = {}
            for (column, index) in columns.items():
                rename = COLUMNS[index]
                value = line[column].strip()

                if rename is 'name':
                    # strip trailing identifier (city, town, etc)
                    value = ' '.join(value.split(' ')[:-1])
                d[rename] = value

            r.append(d)
        return r


def split_states(data):
    split_dict = collections.defaultdict(list)
    for item in data:
        state = item['state']
        split_dict[state].append(item)
    return split_dict


def geojson_feature(place):
    return {
        "type": "Feature",
        "id": place['name'],
        "geometry": {
            "type": "Point",
            "coordinates": [float(place['lon']), float(place['lat'])]
        },
        "properties": {"fips": place['fips']}
    }


def write_out(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = relative_path("../raw/Gaz_places_national.txt")
    try:
        gazeteer = load_gazetteer(fn)
    except IOError:
        print "unable to load", fn
        sys.exit(-1)

    for (abbr, data) in split_states(gazeteer).items():
        state_name = STATES[abbr].replace(' ', '_')

        geojson_collection = {
            "type": "FeatureCollection",
            "features": list()
        }

        for place in data:
            geojson_collection['features'].append(geojson_feature(place))

        print "writing %d places in %s" % (len(data), state_name)
        out_fn = relative_path('../places/%s.geo.json' % state_name)
        write_out(out_fn, geojson_collection)
