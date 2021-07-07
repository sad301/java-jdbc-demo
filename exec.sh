#!/bin/bash

rm -rf files
rm -rf temp
rm -rf ngeprint.db
sqlite3 ngeprint.db ".read ngeprint.sql"
