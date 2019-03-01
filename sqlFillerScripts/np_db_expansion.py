#!/usr/bin/env python
import sqlite3;
import sys; 
import glob;
import os;

def tableReader(sqlTablesPath,databasePath):
    os.chdir(sqlTablesPath);
    db = sqlite3.connect(databasePath);
    cur = db.cursor()
    for sqlFile in glob.glob("*.sql"):
        sqlscript = open(sqlFile,"r"); 
        sql = sqlscript.read();
        cur.executescript(sql);
    db.close()

def main(sqlTablesPath,databasePath):
    tableReader(sqlTablesPath,databasePath);
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2]);

