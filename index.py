#!/usr/bin/env python3

import cgi,cgitb
#connects to mysql

import mysql.connector
from mysql.connector import errorcode
from signup import users
import config
cgitb.enable()
params = cgi.FieldStorage()

def main():
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
    if len(params) == 3:
        #return
        returnval = signup(cursor)
    else:
        #return
        returnval = logon(cursor)
    cursor.close()   #commit the transaction
    cnx.commit()  #this is really important otherwise all changes lost
    #close connection
    cnx.close()
    return returnval
    #quit()


#code for inserting a user
#insertButton = params.getvalue("Sign Up")

#if insert button was pushed
def signup(cursor):
    #get the artist and du to inform them of the time this error occurred, and the actions you performed just before this error.More information about this error may be available in the server errortitle from the form
    user = params.getvalue("user")
    password = params.getvalue("pass")
    name = params.getvalue("name")
    #call the add song function in song to insert the song
    result = users.addUser(cursor, user, name, password)
    #print either a confirmation message or error message
    if result:
        print ('<h2>New user with id ' + str(result) + ' inserted into the database</h2>')
    else:
        print ('<h2>Could not insert the user</h2>')
    #now need to clean up database cursor, etc

    return



#code to log on a USER
def logon(cursor):
    #cursor = connect()
    #get the artist and title from the form
    username = params.getvalue("user")
    password = params.getvalue("pass")
    #call authenticaTeUser
    legit = users.authenticateUser(users, cursor, username, password)

    if (legit):    #user is in database
        #generate a random session ID cookie that has a set expiration date
        print ( "Content-type: text/html" )
        print( "Status: 303 See Other" )
        print( "Location: messageBoard.py" )
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

        #print('<h3>redirect</h3>')
        #return HttpResponseRedirect('messageBoard.html')        #redirect to messageBoard.html
        print("</body></html>")
    else:
    #user is not in database
        print('<h2>Invalid login</h2>')
        quit()

    #now need to clean up database cursor, etc



if __name__ == "__main__":
    main()
