#!/bin/bash

rm -rf ngeprint.db
sqlite3 ngeprint.db ".read ngeprint.sql"
