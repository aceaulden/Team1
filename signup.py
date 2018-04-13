<<<<<<< HEAD
import hashlib
=======
#!/usr/bin/env python3


>>>>>>> refs/remotes/origin/master
# user class- adds, deletes, prints users

class users:
      # This class is used to create and maintain user accounts

      def __init__(self):
        pass

      #add a user to the database
      #songID is AUTO_INCREMENT and votes has a default of 0, so no need to worry about them
      def addUser(self, cursor, user, name, password):
<<<<<<< HEAD
        #Hash the Password
        hash_object = hashlib.sha512(bytes(password, "utf-8"))
        hashPass = hash_object.hexdigest()
        #create query statement
        query = "INSERT INTO Users VALUES (%s, %s, %s);"   # + user + "','" + password + "')"
        #execute the query
        try:
          cursor.execute(query, user, name, hashPass)
=======
        #create query statement
        query = "INSERT INTO Users VALUES (%s, %s, PASSWORD(%s) );"   # + user + "','" + password + "')"
        #execute the query
        try:
          cursor.execute(query, user, name, password)
>>>>>>> refs/remotes/origin/master
          print ("<p> Executed statement: " + cursor.statement + "</p>")
        except mysql.connector.Error as err:
          #for DEBUG only we'll print the error - we should print some generic message instead for production site
          print ('<p style = "color:red">')
          print (err)
          print ('</p>')

          #INSERT INTO Users(Username, Password) VALUES (m197104, PASSWORD('1234') );

        #check number of rows affected > 0 if insert successful
        nbRowsInserted = cursor.rowcount
        userID = cursor.lastrowid #get the last songid inserted

        if nbRowsInserted > 0:

<<<<<<< HEAD
          return user
=======
          return Username
>>>>>>> refs/remotes/origin/master
        else:
          return False

      def authenticateUser(self, cursor, username, password):
<<<<<<< HEAD
          #query = "SELECT Password FROM Users WHERE Username = '%s';"    #gives hashed password in database
          query = "SELECT Password FROM Users WHERE Username = 'm197102';"    #gives hashed password in database
          cursor.execute(query, username)
          hashedpassJK = cursor.fetchone()
          hashedpass = str(hashedpassJK[0])
          #print(hashedpass)
          #print(type(hashedpass))

          if (hashedpass):
              #print("hello laurel " + str(password))
              #query2 = "SELECT PASSWORD(%s) "
              hash_object = hashlib.sha512(bytes(password, "utf-8"))
              givenpass = hash_object.hexdigest()
              #cursor.execute(query2, password)
              #givenpass = cursor.fetchone()
              #print(givenpass)
              #print(type(givenpass))
=======
          query = "SELECT Password FROM Users WHERE Username = '%s';"    #gives hashed password in database
          cursor.execute(query, username)
          hashedpass = cursor.fetchone()

          if (hashedpass):
              query2 = "SELECT PASSWORD(%s); "
              cursor.execeute(query2, password)
              givenpass = cursor.fetchone()
>>>>>>> refs/remotes/origin/master
              if (givenpass == hashedpass):
                  return True
              else:
                  return False
          else:
              return False
<<<<<<< HEAD
=======

>>>>>>> refs/remotes/origin/master
