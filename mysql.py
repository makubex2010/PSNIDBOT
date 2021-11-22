#! /usr/bin/python3

import pymysql

def connectDB(cmd): 
        db = pymysql.connect("bb2d60ffa470c9", "9027fcbf", "us-cdbr-east-04.cleardb.com", "heroku_ec10c9bdacf1022", charset='utf8' )
        cursor = db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
        db.commit()
        db.close()
        return data

def inserttodb(userid, psnid, username = None):
        cmd = "INSERT INTO heroku_ec10c9bdacf1022(userid,psnid,username)VALUES(%d,'%s','%s')" \
        % (userid, pymysql.escape_string(psnid), pymysql.escape_string(username))
        connectDB(cmd)

def changeondb(userid, psnid, username = None):
        cmd = "UPDATE heroku_ec10c9bdacf1022 set psnid='%s' WHERE userid=%d" % (pymysql.escape_string(psnid), userid)
        cmd2 = "UPDATE heroku_ec10c9bdacf1022 set username='%s' WHERE userid=%d" % (pymysql.escape_string(username), userid)
        connectDB(cmd)
        connectDB(cmd2)

def searchname(username):
        cmd = "SELECT psnid FROM heroku_ec10c9bdacf1022 WHERE username='%s'" % username
        data = connectDB(cmd)
        data = ''.join(data)
        return data

def searchindb(userid):
        cmd = "SELECT psnid FROM heroku_ec10c9bdacf1022 WHERE userid=%d" % userid
        data = connectDB(cmd)
        try:
                data = ''.join(data)
        except:
                data = -1
        return data
