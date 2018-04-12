#!/usr/bin/env python3

import cgi,cgitb
#connects to mysql

cgitb.enable()

import mysql.connector
from mysql.connector import errorcode

import config

try:
  cnx = mysql.connector.connect(user=config.USER,
                                password = config.PASSWORD,
                                host = config.HOST,
                                database=config.DATABASE)

except mysql.connector.Error as err:
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

cursor = cnx.cursor()
params = cgi.FieldStorage()

#code for inserting a user
insertButton = params.getvalue("Sign Up")

#if insert button was pushed
if insertButton:
  #get the artist and title from the form
  user = params.getvalue("user")
  password = params.getvalue("pass")

  #call the add song function in song to insert the song
  result = user.addUser(cursor, user, password)
  #print either a confirmation message or error message
  if result:
    print ('<h2>New user with id ' + str(result) + ' inserted into the database</h2>')
  else:
   print ('<h2>Could not insert the user</h2>')
  
  
  
loginButton = params.getvalue("Login")

#if insert button was pushed
if loginButton:
  #get the artist and title from the form
  user = params.getvalue("user")
  password = params.getvalue("pass")
  #call authenticaTeUser
  legit = user.authenticateUser(cursor, user, password)
  if (legit):
    #user is in database
    #redirect to messageBoard.html
  else:
    #user is not in database
    
    
    
#now need to clean up database cursor, etc
cursor.close()
#commit the transaction
cnx.commit()  #this is really important otherwise all changes lost
#close connection
cnx.close()
quit()
