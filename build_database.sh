#!/bin/bash

cp -v people-100.csv /var/lib/mysql-files/
mysql -p < people.sql
