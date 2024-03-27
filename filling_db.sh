#!/bin/sh

psql -U $DB_USER -d $DB_NAME -a -f init.sql