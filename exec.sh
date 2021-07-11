#!/bin/bash

rm -rf files
rm -rf temp
rm -rf ngeprint.db
rm -rf key.txt

sqlite3 ngeprint.db ".read ngeprint.sql"
python3 init.py
