#!/bin/bash

rm -rf files
rm -rf ngeprint.db
sqlite3 ngeprint.db ".read ngeprint.sql"
