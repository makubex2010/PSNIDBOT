#! /usr/bin/python3

import pymysql

def connectDB(cmd): 
        db = pymysql.connect("containers-us-west-21.railway.app", "7012", "root", "eQYm2HwqtWARweRi5g6a", "railway", charset='utf8' )
        cursor = db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
        db.commit()
        db.close()
        return data

def inserttodb(userid, psnid, username = None):
        cmd = "INSERT INTO playstationnetworkid(userid,psnid,username)VALUES(%d,'%s','%s')" \
        % (userid, pymysql.escape_string(psnid), pymysql.escape_string(username))
        connectDB(cmd)

def changeondb(userid, psnid, username = None):
        cmd = "UPDATE playstationnetworkid set psnid='%s' WHERE userid=%d" % (pymysql.escape_string(psnid), userid)
        cmd2 = "UPDATE playstationnetworkid set username='%s' WHERE userid=%d" % (pymysql.escape_string(username), userid)
        connectDB(cmd)
        connectDB(cmd2)

def searchname(username):
        cmd = "SELECT psnid FROM playstationnetworkid WHERE username='%s'" % username
        data = connectDB(cmd)
        data = ''.join(data)
        return data

def searchindb(userid):
        cmd = "SELECT psnid FROM playstationnetworkid WHERE userid=%d" % userid
        data = connectDB(cmd)
        try:
                data = ''.join(data)
        except:
                data = -1
        return data
