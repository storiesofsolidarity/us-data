# US-Data

Contextual geographic and economic data to display on StoriesOfSolidarity.org

## Geography

* Simplified state boundaries and Puerto Rico from [mbostock](http://bl.ocks.org/mbostock/5629120)
* Counties by state from [yooper/open-model](https://github.com/yooper/open-model/tree/master/geodata/topojson/united_states)
* Place names generated from 2015 [US Gazetteer](https://www.census.gov/geo/maps-data/data/gazetteer2015.html) and [converted](geography/scripts/gazetteer.py) to geojson
    * `curl http://www2.census.gov/geo/docs/maps-data/data/gazetteer/2015_Gazetteer/Gaz_place_national.zip -o raw/Gaz_place_national.zip `
    * `unzip raw/Gaz_place_national.zip -d raw`
    * `python scripts/split_places.py`
    
* Zipcode tabulation areas from 2012 [TIGER](http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/), converted to [topojson](https://github.com/mbostock/topojson) and [split](geography/scripts/zipcodes.py) by state and county.
	* `curl http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/tl_2012_us_zcta510.zip -o raw/tl_2012_us_zcta510.zip`
	* `unzip raw/tl_2012_us_zcta510.zip -d raw`
	* ```node --max_old_space_size=8192 `which topojson` -q 1e4 -s 1e-8  -p zip=ZCTA5CE10 -o raw/tl_2012_us_zcta510.topo.json raw/tl_2012_us_zcta510.shp```
	* `curl http://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt -o raw/zcta_county_rel_10.txt`
	* `python scripts/split_zipcodes.py` 

## Economic

* Prevailing wages and Bureau of Labor Statistics via their [API](http://www.bls.gov/developers/home.htm) and custom queries.