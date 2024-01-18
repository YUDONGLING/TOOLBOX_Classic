import os
import sqlite3


def executeDB(DBFolder, DBName, DBQuery, DBParam = ()):
    DBFolder = DBFolder.strip() if DBFolder.strip() != "" else "."
    DBName = DBName.strip()
    DBPath = os.path.join(DBFolder, DBName)
    try:
        DB = sqlite3.connect(DBPath)
        LK = DB.cursor()
        LK.execute(DBQuery, DBParam)
        RS = LK.fetchall()
        DB.commit()
        DB.close()
        return (True, ""), RS
    except Exception as errorMsg:
        return (False, str(errorMsg)), []