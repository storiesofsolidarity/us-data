import sys, csv
from constants import STATE_ABBR
from utils import relative_path, load_csv_columns, split_dict_by, write_json

# map colum names from csv db to output json
ZIPCODE_COLUMNS = {
    'zip': 'zip',
    'primary_city': 'city',
    'acceptable_cities': 'other_cities',
    'state': 'state',
    'county': 'county',
    'latitude': 'lat',
    'longitude': 'lon',
}


def geojson_feature(d):
    return {
        "type": "Feature",
        "id": d['zip'],
        "geometry": {
            "type": "Point",
            "coordinates": [float(d['lon']), float(d['lat'])]
        },
        "properties": {
            "city": d['city'],
            "other_cities": d['other_cities'],
            "state": d['state'],
            "county": d['county'],
        }
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = relative_path("../raw/zip_code_database.csv")
    try:
        zipcode_db = load_csv_columns(fn, ZIPCODE_COLUMNS)
    except IOError:
        print "unable to load", fn
        sys.exit(-1)

    print "loaded %s zipcodes" % len(zipcode_db)
    
    for (abbr, data) in split_dict_by(zipcode_db, 'state').items():
        state_name = STATE_ABBR.get(abbr, '').replace(' ', '_')

        geojson_collection = {
            "type": "FeatureCollection",
            "features": list()
        }

        for place in data:
            geojson_collection['features'].append(geojson_feature(place))

        print "writing %d places in %s" % (len(data), state_name)
        out_fn = relative_path('../zipcodes/%s.geo.json' % state_name)
        write_json(out_fn, geojson_collection)

    print "writing %d places in %s" % (len(zipcode_db), 'all')
    for z in zipcode_db:
        out_fn = relative_path('../zipcodes/all/%s.geo.json' % z['zip'])
        data = geojson_feature(z)
        write_json(out_fn, data)

