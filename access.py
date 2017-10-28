import sqlite3


class access:
    '''
    module responsible for login/signup
    '''

    def __init__(self):

         self.conn = sqlite3.connect("./database.db") #connection to move database
         self.cursor = self.conn.cursor()


    def create_account(self, username, password, password_rpt, address):

        '''
        Checks if username exists in database. If it isn't, return false.
        Function returns true on success.
        '''
        username = username.lower()
        if len(username) < 4:
            print "Username must be atleast 4 characters long"
            return (False, "Username must be atleast 4 characters long")
        if len(address) < 1:
            print "address not entered"
            return (False, "address not entered")
        if (password != password_rpt):
            print "passwords do not match"
            return (False, "passwords do not match")
        if len(password) < 8:
            print "password must be 7 characters"
            return (False, "password must be 7 characters")

        #at this point user field seems okay, test if username exists

        self.cursor.execute("SELECT * FROM customers WHERE name=:usr;",{"usr": username})
        res=self.cursor.fetchall()

        if len(res) > 0:
            print "Username already exists"
            return (False, "account already exists")
        else:
            self.cursor.execute("SELECT MAX(cid) FROM customers;")
            res=self.cursor.fetchone()
            ID = str(int(res[0]) + 1)
            self.cursor.execute("INSERT INTO customers (cid, name, address, pwd) VALUES (?, ?, ?, ?);",
            (ID, username, address, password))
            self.conn.commit()
            print "Account created!"
            return (True, "Account created!")

    def login(self, username, password, customer):

        '''
        Checks if Login credentials are correct. Function returns True on
        success, returns false otherwise
        '''
        username = username.lower()

        if customer:
            self.cursor.execute("SELECT * FROM customers WHERE name=:usr AND pwd=:pwd;", {"usr": username, "pwd": password})
        else:
            self.cursor.execute("SELECT * FROM agents WHERE name=:usr AND pwd=:pwd;", {"usr": username, "pwd": password})
        if self.cursor.fetchone() != None:
            print "Logged in!"
            return (True, "Logged in!")
        else:
            print "username password combo is wrong"
            return (False, "username password combo is wrong")


if __name__ == "__main__":
    a = access()
    #a.create_account("Nick", "13638292", "13638292", "2005 Hilliard Place NW")
    #a.login("bobbylee", "44673111")

    verify = 0
    while (not verify):
    	ID = raw_input("ID: ")
	password = raw_input ("Password: ")
        if (password.isdigit()):
	    password = int(password)
	    verify, v_msg = a.login(ID, password, True)
          
    keywords = []
    






