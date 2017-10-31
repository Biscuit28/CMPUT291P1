import sqlite3
from collections import defaultdict


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

    def login(self, username, password, customer=True):

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


    def search(self, keywords):
        '''
        Querys items based on keywords, assumes keywords is a list
        '''
        products = defaultdict(int)

        for word in keywords:
            SQL = "SELECT * FROM products WHERE name LIKE '%{}%';".format(word)
            self.cursor.execute(SQL)
            results=self.cursor.fetchall()
            for result in results:
                if result[0] not in products:
                    products[result[0]] = 1
                else:
                    products[result[0]] += 1

        products = sorted(products, key=products.get, reverse=True)
        
        print products

if __name__ == "__main__":
    a = access()
    #a.create_account("bobbylee", "4567311", "45673111", "2005 Hilliard Place NW")
    #a.login("bobbylee", "45673111", customer=False)
    a.search(["canned", "beef"])
