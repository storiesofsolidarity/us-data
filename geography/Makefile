clean:
	rm -r raw

# Zip Code Tabulation Areas from Census Tiger data
raw/zip/tl_2012_us_zcta510.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/$(notdir $@)' -o $@.download
	mv $@.download $@

raw/shp/zcta.shp: raw/zip/tl_2012_us_zcta510.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

# ZCTA - County Relations
raw/zcta_county_rel.txt:
	curl 'http://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt' -o $@.download
	mv $@.download $@

# FIPS County names
raw/county_fips.txt:
	curl 'http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt' -o $@.download
	mv $@.download $@.raw
	echo 'STATE,STATEFP,COUNTYFP,COUNTYNAME,CLASSFP' >> raw/county_fips_headers.txt
	cat raw/county_fips_headers.txt $@.raw > $@
	rm raw/county_fips_headers.txt $@.raw

# FIPS State / Territory names
raw/state_fips.txt:
	curl 'http://www2.census.gov/geo/docs/reference/state.txt' -o $@.download
	mv $@.download $@

# ZCTA geojson for all states
raw/zcta/us.geo.json: raw/shp/zcta.shp raw/zcta_county_rel.txt raw/state_fips.txt raw/county_fips.txt
	rm -rf $(dir $@)
	mkdir -p $(dir $@)
	mapshaper raw/shp/zcta.shp \
		-join raw/zcta_county_rel.txt keys="GEOID10:str,ZCTA5:str" fields="ZCTA5:str,STATE:str,COUNTY:str" \
		-join raw/county_fips.txt keys="COUNTY:str,COUNTYFP:str" \
		-join raw/state_fips.txt keys="STATE:str,STATE:str" fields="STATE_NAME" \
		-rename-fields "ZCTA=GEOID10,COUNTY_NAME=COUNTYNAME" \
		-filter-fields "ZCTA,STATE,COUNTY,STATE_NAME,COUNTY_NAME" \
		-filter remove-empty -simplify 15% \
		-o "raw/zcta/us.geo.json" format=geojson id-field="ZCTA"

# split ZCTA geojson into individual states
raw/zcta/state/geo: raw/zcta/us.geo.json
	mkdir -p raw/zcta/state
	mapshaper raw/zcta/us.geo.json \
		-split "STATE_NAME" \
		-o "raw/zcta/state" format=geojson force
	# rename files from raw/zcta/state/us-STATE.json to zcta/state/STATE.geo.json
	@# use shell syntax here, with double-$ to escape from make
	for file in raw/zcta/state/us-*.json; do \
		state=`echo "$$file" | awk -F '[/_\.\-]' '{gsub(" ","_",$$5); print $$5}'`; \
		mv "$$file" raw/zcta/state/$$state.geo.json; \
	done

# create topojson and simplify
zcta/state: raw/zcta/state/geo
	mkdir -p zcta
	@# use shell syntax here, with double-$ to escape from make
	for file in raw/zcta/state/*.geo.json; do \
		state=`echo "$$file" | awk -F '[/\.\-]' '{gsub(" ","_",$$4); print $$4}'`; \
		topojson "$$file" -q 1e6 -s 1e-8 -o "zcta/$$state.topo.json"; \
	done

# Places from US Gazetteer
raw/zip/Gaz_place_national.zip:
	curl 'http://www2.census.gov/geo/docs/maps-data/data/gazetteer/2015_Gazetteer/2015_Gaz_place_national.zip' -o $@.download
	mv $@.download $@
	
raw/gaz_places_national.txt: raw/zip/Gaz_place_national.zip
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

# split by state
places: raw/gaz_places_national.txt
	python scripts/split_places.py
# TODO, convert this to use mapshaper for joins and split
