import sys, csv
from constants import STATE_ABBR
from utils import relative_path, load_csv_columns, split_dict_by, write_json

# map colum names from gazetteer tsv to output json
GAZETTEER_COLUMNS = {
    'USPS': 'state',
    'GEOID': 'fips',
    'NAME': 'name',
    'INTPTLAT': 'lat',
    'INTPTLONG': 'lon',
}


def geojson_feature(place):
    # strip place['name'] trailing identifier (city, town, etc)
    place_name_strip = ' '.join(place['name'].split(' ')[:-1])
    return {
        "type": "Feature",
        "id": place_name_strip,
        "geometry": {
            "type": "Point",
            "coordinates": [float(place['lon']), float(place['lat'])]
        },
        "properties": {"fips": place['fips']}
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = relative_path("../raw/Gaz_places_national.txt")
    try:
        gazetteer = load_csv_columns(fn, GAZETTEER_COLUMNS, delimiter='\t', quoting=csv.QUOTE_NONE)
    except IOError:
        print "unable to load", fn
        sys.exit(-1)

    for (abbr, data) in split_dict_by(gazetteer, 'state').items():
        state_name = STATE_ABBR[abbr].replace(' ', '_')

        geojson_collection = {
            "type": "FeatureCollection",
            "features": list()
        }

        for place in data:
            geojson_collection['features'].append(geojson_feature(place))

        print "writing %d places in %s" % (len(data), state_name)
        out_fn = relative_path('../places/%s.geo.json' % state_name)
        write_json(out_fn, geojson_collection)
