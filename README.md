parku
=====

City of Melbourne Parking Spaces Project for infraHack 2014

How do the objects that you buy get into the city?
Buisnesses use logistics applications to optimise the last mile frieght.
Parku is simple and effective.
It is an improved API to the city of melbourne street parking sensors which combines the geographic and real-time sensor data that the city of melbourne provide*.
We have also developed a simple map which shows how the API works and provides a useful interface for searching for areas.

* This is an area for improvement for the city of melbourne 

Ubuntu dependencies
-------------------

apt-get install apache2 postgresql-client-9.3 postgresql-9.3-postgis-2.1 

Python dependencies
-------------------

pip install django psycopg2

PostgreSQL setup
----------------

sudo su - postgres
createuser -P <username>
createdb <db_name>
psql -d <db_name> -c "CREATE EXTENSION postgis;"

