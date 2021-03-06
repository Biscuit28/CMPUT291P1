import sqlite3
from collections import defaultdict


class access:

    '''
    module responsible for login/signup and general search
    '''

    def __init__(self):

         self.conn = sqlite3.connect("./database.db") #connection to move database
         self.cursor = self.conn.cursor()


    def create_account(self, username, password, password_rpt, address):

        '''
        Checks if username exists in database.

        Args: username (str), password (str), password_rpt(Str), address(str)
        Returns: (success (boolean), message (str)) (tuple)
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
            self.cursor.execute("SELECT MAX(CAST(substr(cid, 2) AS int)) FROM customers;")
            res=self.cursor.fetchone()
            ID = "c"+str(int(res[0]) + 1)
            self.cursor.execute("INSERT INTO customers (cid, name, address, pwd) VALUES (?, ?, ?, ?);",
            (ID, username, address, password))
            self.conn.commit()
            print "Account created!"
            return (True, "Account created!")


    def login(self, username, password, customer=True):

        '''
        Checks if Login credentials are correct.

        Args: username (str), password (str), customer (varargs, boolean)
        Returns: (success (boolean), message (str)) (tuple)
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


    def search(self, keywords):                                                 #NOTE there is a issue if the user enters an empty string

        '''
        Querys items based on keywords, assumes keywords is a list

        Args: keywords (list (str))
        Returns: sorted product_ids (list)
        '''
        products = defaultdict(int)
        if keywords==[]:
            SQL="SELECT * FROM products;"
            self.cursor.execute(SQL)
            ret_list=[]
            for x in self.cursor.fetchall():
                ret_list.append(x[0])
            return ret_list
        else:
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

        Args: products (list of pid's)
        Returns: product info (list)
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
        q2 = "SELECT prd.pid, COUNT(crr.sid) AS q2 FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE"+cond[:-2]+" GROUP BY prd.pid"

        #query 3 - the number of stores that have it in stock
        q3 = "SELECT prd.pid, COUNT(crr.sid) AS q3 FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE"+cond[:-2]+" AND crr.qty > 0 GROUP BY prd.pid"

        #query 4 - the minimum price among the stores that carry it
        q4 = "SELECT prd.pid, MIN(crr.uprice) AS uprice FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE" +cond[:-2] + " GROUP BY crr.pid"

        #query 5 - the minimum price among the stores that have the product in stock
        q5 = "SELECT prd.pid, MIN(crr.uprice) AS uprice FROM products prd, carries crr ON prd.pid=crr.pid \
        WHERE" +cond[:-2] + " GROUP BY crr.pid HAVING crr.qty>0"

        #query 6 - the number of orders within the past 7 days ??
        q6 = "SELECT oln.pid, COUNT(oln.oid) AS q6 FROM orders ord, olines oln ON ord.oid=oln.oid \
        WHERE ord.odate BETWEEN DATETIME('now') AND DATETIME('now', '-7 day') AND" +cond2[:-2]+" GROUP BY oln.pid"
        #print q6

        #main
        main = "SELECT a.pid, a.name, a.unit, IFNULL(b.q2, 0), IFNULL(c.q3, 0), IFNULL(d.uprice, 'NA'), IFNULL(e.uprice, 'NA'), IFNULL(f.q6, 0) \
        FROM ((((({}) a LEFT OUTER JOIN ({}) b USING (pid)) LEFT OUTER JOIN ({}) c \
        USING (pid)) LEFT OUTER JOIN ({}) d USING (pid)) LEFT OUTER JOIN ({}) e USING (pid)) \
        LEFT OUTER JOIN ({}) f USING (pid);".format(q1, q2, q3, q4, q5, q6)

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

        Args: product_id (str)
        Returns: (product detial (list), store info (list))
        '''
        SQL = "SELECT prd.pid, prd.name, prd.unit, prd.cat FROM products prd \
        WHERE prd.pid = '{}';".format(product_id)
        self.cursor.execute(SQL)
        t1 = self.cursor.fetchall()

        q1 = "SELECT str.sid, str.name, crr.uprice, crr.qty \
        FROM products prd, carries crr, stores str ON prd.pid=crr.pid \
        AND str.sid=crr.sid WHERE prd.pid='{}'".format(product_id)

        q2="SELECT oln.sid, SUM(oln.qty) AS tot FROM olines oln, orders ord ON oln.oid=ord.oid \
        WHERE oln.pid='{}' AND 7>=JULIANDAY('now')-JULIANDAY(ord.odate) GROUP BY oln.sid".format(product_id)

        SQL="SELECT a.sid, a.name, a.uprice, a.qty,IFNULL(b.tot, 0) FROM ({}) a \
        LEFT OUTER JOIN ({}) b USING (sid) ORDER BY a.qty > 0, a.uprice ASC;".format(q1, q2)

        self.cursor.execute(SQL)
        t2 = self.cursor.fetchall()
        return (t1, t2)




if __name__ == "__main__":
    a = access()
    # a.create_account("bobbymee", "45673111", "45673111", "2005 Hilliard Place NW")
    # a.login("bobbylee", "45673111", customer=False)
    # r= a.search(["e"])
    # x = a.get_products(r)
    # for i in x:
    #     print i
    x2 = a.product_details('p3')
    for i in x2[0]:
        print i
    print "store details"
    for i in x2[1]:
        print i
