@echo off

del ngeprint.db
sqlite3 ngeprint.db ".read ngeprint.sql"
