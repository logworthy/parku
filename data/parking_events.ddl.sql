CREATE TABLE parking_events
(
    id INT,
    areaname VARCHAR,
    streetname VARCHAR,
    betweenstreet1 VARCHAR,
    betweenstreet2 VARCHAR,
    sideofstreet VARCHAR,
    streetmarker VARCHAR,
    arrivaltime TIMESTAMP,
    departuretime TIMESTAMP,
    durationseconds NUMERIC(1000),
    sign VARCHAR,
    inviolation VARCHAR,
    streetid INT,
    deviceid INT
);

