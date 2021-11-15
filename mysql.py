#! /usr/bin/python3

import pymysql

def connectDB(cmd):
        db = pymysql.connect("s465z7sj4pwhp7fn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com", "3306", "u0oumepy212w7hrd", "lmhzodresmb5a1dr", "wagjozo03g4tc27f", charset='utf8' )
        cursor = db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
        db.commit()
        db.close()
        return data
