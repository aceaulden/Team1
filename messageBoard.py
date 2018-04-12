#!/usr/bin/env python3
import config #config file
import mysql.connector #database connector
from mysql.connector import errorcode #error for mysql
import hashlib, time, os, shelve, cgi
from http import cookies
import cgitb

cgitb.enable()

form = cgi.FieldStorage() # only needs to be instantiated once

try:
  '''cnx = mysql.connector.connect(user='theuser',
                                password = 'thepassword',
                                host = 'thehostserver',
                                database='thedatabase')'''
  cnx = mysql.connector.connect(user=config.USER,
                                password = config.PASSWORD,
                                host = config.HOST,
                                database=config.DATABASE)
				#connect to database using config.py parameters

#check for errors
except mysql.connector.Error as err:
  #If we have an error connecting to the database we would like to output this fact.
  #This requires that we output the HTTP headers and some HTML.
  print ( "Content-type: text/html" )
  print()
  print ("""\
  <!DOCTYPE html>
  <html>
  <head>
  <meta charset = "utf-8">
  <title>DB connection with Python</title>
  <style type = "text/css">
  table, td, th {border:1px solid black}
  </style>
  </head>
  <body>
  """)
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
  print("<p>Fix your code or Contact the system admin</p></body></html>")
  quit()
#create cursor to send queries
cursor = cnx.cursor()


def sessionAuthenticate():
    cookie = cookies.SimpleCookie()
    string_cookie = os.environ.get('HTTP_COOKIE')
    issession = False
    sid=0
    if not string_cookie:
       message = 'No cookie - no session'
       return(issession,sid)
    else:
       cookie.load(string_cookie)
       if 'sid' in cookie:
         sid = cookie['sid'].value
         issession=True
         message ="<p>Found session - will read lastvisit</p>"
         return(issession,sid)
       else:
         message = '<p>No sid - no session </p>'
         return(issession,sid)

def generateMessageBoard():
    HTML = "<h2> Welcome To A Better Facebook </h2>"
    #parse database for stored messages from Messages table
    query = "SELECT * from Messages ORDER BY Timestamp ASC"  #query to get all messages
    cursor.execute(query) 
    for (Username,Timestamp,Message) in cursor:#goes through message table one by one
        HTML += "\n<div class=\"container\">"
        HTML += "\n<img src=\"" + USRIMG + "\"alt=\"Avatar\" style=\"width:100%;\">"
        HTML += "\n<p>" + Message + "</p>"
        HTML += "\n<span clgass=\"time-right\">" + Timestamp + "</span>"
        HTML += "\n</div>"
    return HTML #return full HTML string
def addUserLog():
        USRMSG= form.getValue("message")
        USRTIME= form.getValue("time")
        query = "SELECT * FROM UserInfo WHERE sessionid = %s ;"
        cursor.execute(query,sid)
        for row in cursor:
            print(row)
def deleteMessage(): #this will 

def main():
	(issession,sid) = sessionAuthenticate()       
	print(issession)
	print(sid)



main()     
