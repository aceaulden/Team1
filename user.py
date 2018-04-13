
# user class- adds, deletes, prints users

class user:
  # This class is used to create and maintain user accounts

  def __init__(self):
    pass

  #add a user to the database
  #songID is AUTO_INCREMENT and votes has a default of 0, so no need to worry about them
  def addUser(cursor, user, password):
    #create query statement
    query = "Insert into Users(Username, Password) values (%s, PASSWORD(%s) )"   # + user + "','" + password + "')"
    #execute the query
    try:
      cursor.execute(query, user, password) 
      print ("<p> Executed statement: " + cursor.statement + "</p>")
    except mysql.connector.Error as err:
      #for DEBUG only we'll print the error - we should print some generic message instead for production site
      print ('<p style = "color:red">')
      print (err)
      print ('</p>')

    #check number of rows affected > 0 if insert successful
    nbRowsInserted = cursor.rowcount
    userID = cursor.lastrowid #get the last songid inserted

    if nbRowsInserted > 0:

      return Username
    else:
      return False

def authenticateUser(cursor, user, pass): 
  #if user and pass is correct and in database return True
  query = "SELECT Password FROM Users WHERE Username = %s'    #gives hashed password in database
  cursor.execute(query, user)
  hashedpass = cursor.lastrow
  if (hashedpass == Null):
    return False
  query2 = "SELECT PASSWORD(%s); "
  cursor.execeute(query2, pass)
  givenpass = cursor.lastrow
  if (givenpass == hashedpass):
    return True
  else:
    return False
    
"""
  def printUsers(cursor):
    query = "SELECT userID, user, pass FROM Users ORDER BY user"
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
    
  
    table = "<table><tr><th>userID</th><th>Artist</th><th>Title</th><th>Votes</th></tr>\n"
    for (songID, artist, title, votes) in cursor:
    # for (artist,) in cursor: #do something like this if only one column, artist in the example, is returned - needs to be a tuple, so have the ,
       table += "<tr><td>"+str(songID) + "</td><td>" + artist+"</td><td>"+title+"</td><td>" + str(votes) + "</td></tr>\n"
       nbRows+=1
    table += "</table>"

    if nbRows > 0:
      return table
    else:
      return ""
