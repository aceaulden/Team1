import hashlib, time, os, shelve
from http import cookies

import cgitb;

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
    for x in y:
        HTML += "\n<div class=\"container\">"
        HTML += "\n<img src=\"" + USRIMG + "\"alt=\"Avatar\" style=\"width:100%;\">"
        HTML += "\n<p>" + USRMSG + "</p>"
        HTML += "\n<span clgass=\"time-right\">" + USRTIME + "</span>"
        HTML += "\n</div>"

def addUserLog():
        USRMSG= form.getValue("message")
        USRTIME= form.getValue("time")
        query = "SELECT * FROM UserInfo WHERE sessionid = %s ;"
        cursor.execute(query,sid)
        for row in cursor:
            print(row)
            
