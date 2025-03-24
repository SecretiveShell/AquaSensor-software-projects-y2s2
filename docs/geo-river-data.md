# How to download river data

1) download `https://download.geofabrik.de/europe/great-britain-latest.osm.pbf`

2) use osmconvert to run `osmconvert great-britain-latest.osm.pbf -o=gb.osm`

3) use osmfilter to run `osmfilter gb.osm --keep="waterway=river" > rivers.osm`