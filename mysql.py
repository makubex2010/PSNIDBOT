#! /usr/bin/python3

import pymysql

def connectDB(cmd): 
        db = pymysql.connect("mysql://u0oumepy212w7hrd:lmhzodresmb5a1dr@s465z7sj4pwhp7fn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/wagjozo03g4tc27f")
        cursor = db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
        db.commit()
        db.close()
        return data

def inserttodb(userid, psnid, username = None):
        cmd = "INSERT INTO PlayStation-Networkid(userid,psnid,username)VALUES(%d,'%s','%s')" \
        % (userid, pymysql.escape_string(psnid), pymysql.escape_string(username))
        connectDB(cmd)

def changeondb(userid, psnid, username = None):
        cmd = "UPDATE PlayStation-Networkid set psnid='%s' WHERE userid=%d" % (pymysql.escape_string(psnid), userid)
        cmd2 = "UPDATE PlayStation-Networkid set username='%s' WHERE userid=%d" % (pymysql.escape_string(username), userid)
        connectDB(cmd)
        connectDB(cmd2)

def searchname(username):
        cmd = "SELECT psnid FROM PlayStation-Networkid WHERE username='%s'" % username
        data = connectDB(cmd)
        data = ''.join(data)
        return data

def searchindb(userid):
        cmd = "SELECT psnid FROM PlayStation-Networkid WHERE userid=%d" % userid
        data = connectDB(cmd)
        try:
                data = ''.join(data)
        except:
                data = -1
        return data
