#!/bin/bash

DB_USER=parku

psql -U $DB_USER -f parking_events.ddl.sql
