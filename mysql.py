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

def inserttodb(userid, liveid, username = None):
        cmd = "INSERT INTO xboxliveid(userid,liveid,username)VALUES(%d,'%s','%s')" \
        % (userid, pymysql.escape_string(liveid), pymysql.escape_string(username))
        connectDB(cmd)

def changeondb(userid, liveid, username = None):
        cmd = "UPDATE xboxliveid set liveid='%s' WHERE userid=%d" % (pymysql.escape_string(liveid), userid)
        cmd2 = "UPDATE xboxliveid set username='%s' WHERE userid=%d" % (pymysql.escape_string(username), userid)
        connectDB(cmd)
        connectDB(cmd2)

def searchname(username):
        cmd = "SELECT liveid FROM xboxliveid WHERE username='%s'" % username
        data = connectDB(cmd)
        data = ''.join(data)
        return data

def searchindb(userid):
        cmd = "SELECT liveid FROM xboxliveid WHERE userid=%d" % userid
        data = connectDB(cmd)
        try:
                data = ''.join(data)
        except:
                data = -1
        return data
