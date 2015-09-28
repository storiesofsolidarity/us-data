import sys
from constants import STATE_FIPS
from utils import (relative_path, load_csv_columns,
    split_dict_by, build_dict,
    write_json, read_json)

# map colum names from census tsv to output json
ZCTA_COLUMNS = {
    'ZCTA5': 'zcta',
    'STATE': 'state',
    'COUNTY': 'county',
}


def topojson_feature(zcta):
    return {
        "type": zcta['type'],
        "id": zcta['id'],
        "arcs": zcta['arcs'],
        "properties": {"county": zcta['properties']['county'],
                       "state": zcta['properties']['state']}
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn_zcta = sys.argv[1]
        fn_counties = sys.argv[2]
    else:
        fn_zcta = relative_path("../raw/tl_2012_us_zcta510.topo.json")
        fn_counties = relative_path("../raw/zcta_county_rel_10.txt")

    try:
        zcta_file = read_json(fn_zcta)
        zcta_data = zcta_file['objects']['tl_2012_us_zcta510']['geometries']
        counties_data = load_csv_columns(fn_counties, ZCTA_COLUMNS)

    except IOError:
        print "unable to load files", fn_zcta, fn_counties
        sys.exit(-1)

    # merge zcta_data with counties_data
    counties_dict = build_dict(counties_data, 'zcta')
    zcta_merged = []
    for zcta in zcta_data:
        zip_id = zcta['properties']['zip']
        try:
            county = counties_dict[zip_id]
            zcta['properties']['county'] = county['county']  # actually a fips id
            zcta['properties']['state'] = county['state']  # ditto
        except KeyError:
            print "%s not in counties_dict" % zip_id

        # move zip_id from properties to object id
        zcta['id'] = zip_id
        del zcta['properties']['zip']

        zcta_merged.append(zcta)

    for (fips, data) in split_dict_by(zcta_merged, 'properties', 'state').items():
        state_name = STATE_FIPS[fips]

        geojson_collection = {
            "type": "GeometryCollection",
            "geometries": list()
        }

        for zcta in data:
            geojson_collection['geometries'].append(topojson_feature(zcta))

        print "writing %d ZCTAs in %s" % (len(data), state_name)
        out_fn = relative_path('../zcta/%s.topo.json' % state_name.replace(' ', '_'))
        write_json(out_fn, geojson_collection)
