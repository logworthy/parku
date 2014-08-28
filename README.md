parku
=====

City of Melbourne Parking Spaces Project for infraHack 2014

Python dependencies
-------------------

pip install \
	django \
	psycopg2 \
	gdal 

PostgreSQL setup
----------------

sudo su - postgres
createuser -P <username>
createdb <db_name>
psql -d <db_name> -c "CREATE EXTENSION postgis;"
