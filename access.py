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
        return sorted(products, key=products.get, reverse=True)


    def get_products(self, products):
        '''
        Takes in a list of products, and finds the details according to the
        following specification:

        For each matching product, list the product id, name, unit, the number
        of stores that carry it, the number of stores that have it in stock, the
        minimum price among the stores that carry it, the minimum price among the
        stores that have the product in stock, and the number of orders within the past 7 days.
        '''
        #initialize condition
        cond = ""
        cond2 = ""
        for prd in products:
            cond += " prd.pid='{}' OR".format(prd)
            cond2 += " oln.pid='{}' OR".format(prd)

        #query 1 - product id, name, unit
        q1 = "SELECT prd.pid, prd.name, prd.unit FROM products prd \
        WHERE"+cond[:-2]

        #query 2 - number of stores that carry it
        q2 = "SELECT prd.pid, COUNT(crr.sid) FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE"+cond[:-2]+" GROUP BY prd.pid"

        #query 3 - the number of stores that have it in stock
        q3 = "SELECT prd.pid, COUNT(crr.sid) FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE"+cond[:-2]+" AND crr.qty > 0 GROUP BY prd.pid"

        #query 4 - the minimum price among the stores that carry it
        q4 = "SELECT prd.pid, crr.uprice FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE" +cond[:-2] + " AND crr.uprice = (SELECT MIN(crr2.uprice) FROM carries crr2 WHERE crr.pid=crr2.pid)"

        #query 5 - the number of orders within the past 7 days
        q5 = "SELECT prd.pid, crr.uprice FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE" +cond[:-2] + " AND crr.uprice = (SELECT MIN(crr2.uprice) FROM carries crr2 WHERE crr.pid=crr2.pid AND crr.qty > 0)"

        #query 6 - the number of orders within the past 7 days ??
        q6 = "SELECT oln.pid, COUNT(oln.oid) FROM orders ord, olines oln ON ord.oid=oln.oid \
        WHERE ord.odate BETWEEN DATETIME('now') AND DATETIME('now', '-7 day') AND" +cond2[:-2]+" GROUP BY oln.pid"
        #print q6
        #main
        main = "SELECT * FROM ((((({}) LEFT OUTER JOIN ({}) USING (pid)) LEFT OUTER JOIN ({}) \
        USING (pid)) LEFT OUTER JOIN ({}) USING (pid)) LEFT OUTER JOIN ({}) USING (pid)) \
        LEFT OUTER JOIN ({}) USING (pid);".format(q1, q2, q3, q4, q5, q6)

        self.cursor.execute(main)
        return self.cursor.fetchall()


    def product_details(self, product_id):
        '''
        Takes in a product ID and returns the details of that product. the
        details returned should adhere to the following specification

        product id, name, unit, category and a listing of all stores that carry
        the product with their prices, quantities in stock and the number of orders
        within the past 7 days. If a product is carried by more than one store,
        the result should be ordered as follows:

        (1) the stores that have the product in stock will be listed before those that don't;

        (2) the stores in each case will be sorted based on the store price (from lowest to highest).
        '''

        pass



if __name__ == "__main__":
    a = access()
    #a.create_account("bobbylee", "4567311", "45673111", "2005 Hilliard Place NW")
    #a.login("bobbylee", "45673111", customer=False)
    r= a.search(["canned", "beef"])
    a.get_products(r)
