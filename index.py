#!/usr/bin/env python3

import cgi,cgitb
#from song import song

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


insertButton = params.getvalue("Submit")



if insertButton:
    username = params.getvalue("username")
    password = hash(params.getvalue("password"))
    result = song.addUser(username, password)
    if result==1:
        #result is Success so a new entry was added to the database.
        #Instead of displaying this fact, we redirect to the page.
        #This sets off the Redirect portion of the POST / Redirect / GET action.
        #The GET action happens at the browser when it gets the Redirect.
        ##print ('<h2>New song with id ' + str(result) + ' inserted into the database</h2>')
        print('Status: 303 See Other')
        print('Location: index.py')
        print('Content-type: text/html')
        print()
        #Note, we do not stop execution at this point, there is some clean up to do that
        #is common with the action in the else statement so it follows that.
      else:
       #So if we get to this part of the code it means that the insert failed.
       #We need to print HTTP Headers and content.
       print('Content-type: text/html')
       print()
       print ("""\
       <!DOCTYPE html>
       <html>
       <head>
       <meta charset = "utf-8">
       <meta http-equiv="refresh" content="5; url=index.py">
       <title>DB connection Error</title>
       <style type = "text/css">
       table, td, th {border:1px solid black}
       </style>
       </head>
       <body>
       """)
       print ('<h2>Could not add user </h2>')
       #Now we branch depending on the error code encountered.
       if result == 0:
          print ('<p>Sorry, something unexpected happened when we tried to add the song to the database. You will be redirected to the song list shortly.</p>')


      #now need to clean up database cursor, etc
      cursor.close()
      #commit the transaction
      cnx.commit()  #this is really important otherwise all changes lost
      #close connection
      cnx.close()
      quit()
