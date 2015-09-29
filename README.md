# US-Data

Contextual geographic and economic data to display on StoriesOfSolidarity.org

## Geography

* Simplified state boundaries and Puerto Rico from [mbostock](http://bl.ocks.org/mbostock/5629120)
* Counties by state from [yooper/open-model](https://github.com/yooper/open-model/tree/master/geodata/topojson/united_states)
* Place names generated from 2015 [US Gazetteer](https://www.census.gov/geo/maps-data/data/gazetteer2015.html) and [split](geography/scripts/split_places.py) by state as geojson.
    * `make places`
* Zipcode tabulation areas from 2012 [TIGER](http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/) data, joined to [Census Relationship Files](https://www.census.gov/geo/maps-data/data/relationship.html) and converted to geojson by state with [mapshaper](https://github.com/mbloch/mapshaper), and simplified to [topojson](https://github.com/mbostock/topojson).
	* `make zcta/state/topo`

## Economic

* Prevailing wages and Bureau of Labor Statistics via their [API](http://www.bls.gov/developers/home.htm) and custom queries.