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
    result = user.addUser(username, password)
    if result==1:
        #result is Success so a new entry was added to the database.
        #Instead of displaying this fact, we redirect to the page.
        #This sets off the Redirect portion of the POST / Redirect / GET action.
        #The GET action happens at the browser when it gets the Redirect.
        ##print ('<h2>New user with id ' + str(result) + ' inserted into the database</h2>')
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
          print ('<p>Sorry, something unexpected happened when we tried to add the user to the database. You will be redirected to the song list shortly.</p>')


      #now need to clean up database cursor, etc
      cursor.close()
      #commit the transaction
      cnx.commit()  #this is really important otherwise all changes lost
      #close connection
      cnx.close()
      quit()


#------------------------------------------------------
# user class- adds, deletes, prints users

class user:
  # This class is used to create and maintain user accounts

  def __init__(self):
    pass

  #add a song to the database
  #songID is AUTO_INCREMENT and votes has a default of 0, so no need to worry about them
  def addSong(cursor, artist, title):
    #create query statement
    query = "Insert into songs(artist, title) values ('" + artist + "','" + title + "')"
    #execute the query
    try:
      cursor.execute(query) 
      print ("<p> Executed statement: " + cursor.statement + "</p>")
    except mysql.connector.Error as err:
      #for DEBUG only we'll print the error - we should print some generic message instead for production site
      print ('<p style = "color:red">')
      print (err)
      print ('</p>')

    #check number of rows affected > 0 if insert successful
    nbRowsInserted = cursor.rowcount
    songID = cursor.lastrowid #get the last songid inserted

    if nbRowsInserted > 0:

      return songID
    else:
      return False


  def printSongs(cursor):
    query = "SELECT SongID, Artist, Title, Votes FROM songs ORDER BY Artist, Title"
    # query = "SELECT Artist FROM songs ORDER BY Artist, Title"  # if only one column returned, make sure we read it as a tuple of 1 element, which is (col1,)
    try:
      cursor.execute(query)
    except mysql.connector.Error as err:
      #for DEBUG only we'll print the error and statement- we should print some generic message instead for production site
      print ('<p style = "color:red">')
      print(err)
      print (" for statement" + cursor.statement )
      print ('</p>')

    nbRows = 0
    #create a table with results
    table = "<table><tr><th>SongID</th><th>Artist</th><th>Title</th><th>Votes</th></tr>\n"
    for (songID, artist, title, votes) in cursor:
    # for (artist,) in cursor: #do something like this if only one column, artist in the example, is returned - needs to be a tuple, so have the ,
       table += "<tr><td>"+str(songID) + "</td><td>" + artist+"</td><td>"+title+"</td><td>" + str(votes) + "</td></tr>\n"
       nbRows+=1
    table += "</table>"

    if nbRows > 0:
      return table
    else:
      return ""
