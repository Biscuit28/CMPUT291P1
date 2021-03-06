import sqlite3
import sys
import access
import getpass
from customer import customer
from collections import defaultdict

class access:
    '''
    module responsible for login/signup and general search
    '''

    def __init__(self):

         self.conn = sqlite3.connect("./database.db") #connection to move database
         self.cursor = self.conn.cursor()
         self.user_typ = -1


    def create_account(self):

        '''
        Checks if username exists in database.

        Args: username (str), password (str), password_rpt(Str), address(str)
        Returns: (success (boolean), message (str)) (tuple)
        '''


        # Get username AND check viability
        while (True):
            username = raw_input("Create username: ").lower()
            if len(username) < 4:
                print "Username must be atleast 4 characters long"
            else:
                # Username is long enough
                self.cursor.execute("SELECT * FROM customers WHERE name=:usr;",{"usr": username})
                res=self.cursor.fetchall()
                if len(res) == 0:
                    # Username is available
                    break
                else:
                    print "Username already exists"

        # Get password AND check it
        while (True):
            password = raw_input("Create password: ")
            password_rpt = raw_input("Type password again: ")
            if (len(password) < 7):
                print "password must be 7 characters"
            elif (password == password_rpt):
                break

        # Get address AND check it
        while (True):
            address = raw_input("Home Address: ")
            if (len(address) == 0):
                print "address not entered"
            else:
                break

        '''
        #username = username.lower()
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
        '''


        self.cursor.execute("SELECT * FROM customers WHERE name=:usr;",{"usr": username})
        res=self.cursor.fetchall()
        #if len(res) > 0:
        #    print "Username already exists"
        #    return (False, "account already exists")

        # If program gets to here, user information should be okay (already validated)
        self.cursor.execute("SELECT MAX(cast(substr(cid, 2) as int)) FROM customers;")
        res=self.cursor.fetchone()
        print res
        #ID = str(int(res[0][1:]) + 1)
        ID = str(res[0] + 1)
        print ID
        ID = ''.join(('c', ID))
        self.cursor.execute("INSERT INTO customers (cid, name, address, pwd) VALUES (?, ?, ?, ?);",
        (ID, username, address, password))
        self.conn.commit()
        print "Account created!"
        return (True, "Account created!")


    def login(self, user_typ, username, password):
        '''
        Checks if Login credentials are correct.

        Args: username (str), password (str), customer (varargs, boolean)
        Returns: (success (boolean), message (str)) (tuple)
        '''
        #while (True):
            #user_typ = input("Type 1 for customer login or 0 for agent login: ")
            #username = str(raw_input("Username: ").lower()).rstrip()
            #password = str(raw_input("Password: "))
        if user_typ == 1:
            self.cursor.execute("SELECT * FROM customers WHERE name=? AND pwd=?", (username, password))
        elif user_typ == 0:
            self.cursor.execute("SELECT * FROM agents WHERE name=? AND pwd=?", (username, password))

        if self.cursor.fetchone() != None:
            print "Logged in!"
            return (True, "Logged in!")
            #break
        else:
            print "username password combo is wrong"
            return (False, "username password combo is wrong")


    def search(self, keywords):

        '''
        Querys items based on keywords, assumes keywords is a list

        Args: keywords (list (str))
        Returns: sorted product_ids (list)
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
        For each matching product, list the:
        0.) product id
        1.) name
        2.) unit,
        3.) the number of stores that carry it,
        4.) the number of stores that have it in stock,
        5.) the minimum price among the stores that carry it,

        6.) the minimum price among the stores that have the product in stock,
        7.) and the number of orders within the past 7 days.
        '''
        # Argument: pid (assume pid exists)
        # returns:
        #    a list pd which follows the form, None is placed in query position if nothing comes back
        #    example pd = [u'p9', u'300ml dishwashing liquid', u'ea', 1, 6.0, 1, 6.0, None]
        #    None in postion 7 because no orders within past 7 days
        #    [u'p10', u'400ml canned beef ravioli', u'ea', None, None, None]
        #    first None represent no stores carry/no min price, etc
        pd = []
        # 0, 1, 2
        q1 = "SELECT prd.pid, prd.name, prd.unit FROM products prd \
        WHERE prd.pid = '{}';".format(product_id)

        # 3, 5
        q2 = "SELECT count(pid), min(uprice) FROM carries WHERE pid = '{}' \
        GROUP BY pid".format(product_id)

        # 4, 6
        q3 = "SELECT count(pid), min(uprice) FROM carries WHERE \
        pid = '{}' AND qty <> 0 GROUP BY pid".format(product_id)

        # 7
        q4="SELECT oln.sid, SUM(oln.qty) AS tot FROM olines oln, orders ord ON oln.oid=ord.oid \
        WHERE oln.pid='{}' AND 7>=JULIANDAY('now')-JULIANDAY(ord.odate) GROUP BY oln.sid".format(product_id)

        queries = [q1, q2, q3, q4]
        for q in queries:
            self.cursor.execute(q)
            qr = self.cursor.fetchone() # should work as fetch one aswell

            if qr == None:
                pd.append(None)

            else:
                for el in qr:
                    pd.append(el)
        return pd




    def more_product_details(self, product_id):

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
        #print ("|{}|{}|{}|{}|".format(t1[0], t1[1], t1[2], len(t2)))
        return (t1, t2)

    def make_customer(self, username):
            self.cursor.execute("SELECT * FROM customers WHERE name=?", username)
            r = self.cursor.fetchone()
            print r
            cid, address = r[0], r[2]
            u = customer(cid, username, address, password)

    def ui_Login(self):
        # used function login, but formats nicely for ui
        # --> 3 attempts and checks user_typ is 1 or 0
        while (True):
            #user_typ = input("Type 1 for customer login or 0 for agent login: ")
            #print("Type 1 for customer login or 0 for agent login: ")
            #user_typ = self.get_input("Type 1 for customer login or 0 for agent login: ")
            user_typ = self.get_input("Type 1 for customer login or 0 for agent login: ")
            if (user_typ in [0,1]):
                break
        for attempt in range(3):
            # Use Raw input here (dont use get_input function)
            print("Login Attempts Remaining: [{}]".format(2-attempt))
            username = str(raw_input("-->Username: ").lower()).rstrip()
            #password = str(raw_input("-->Password: "))
            password = getpass.getpass("-->Password: ")
            verified = self.login(user_typ, username, password)[0]
            if (verified):
                return (True, user_typ, username)

        return False

    def inp_help(self):
        print("commands can be used on any line that does not have an arrow (-->)")
        commands = ["--help", "--quit", "--search", "--login", "--logout", "--signup"]
        for command in commands:
            print(command)

    def inp_quit(self):
        print("Have nice day!")
        raise SystemExit

    def inp_search(self):
        # if user is customer

        if (self.user_typ == 1):
            searchInput = self.get_input("Searchbar: ")
            searchInput = searchInput.split()
            r= self.search(searchInput)
            self.display_search_results(r)
        else:
            print ("Please log in as customer to use search feature.")

    def inp_login(self):
        # login
        verified = self.ui_Login()
        if (verified == False):
            print "Max attempts reached, please try again later!"
            raise SystemExit
        self.user_typ = 1
        return verified

    def inp_logout(self):
        self.user_typ = -1
        return uiTest()

    def inp_signup(self):

        if (self.user_typ != -1):
            print ("Please logout before making new account")

        else:
            self.create_account()
            return uiTest()


    def get_input(self, message):
        # Function to use when getting input from user
        # checks is input is a command from user, if not, return output as is
        # output will always be string so if we want to return other type, must check and change (eg int)
        #cMap = {"--help":self.inp_help, "--quit":self.inp_quit, "--logout":self.inp_logout}
        cMap = {"--help":self.inp_help, "--quit":self.inp_quit, "--search":self.inp_search, "--login":self.inp_login, "--logout":self.inp_logout, "--signup":self.inp_signup}
        while True:
            inp = raw_input(message).rstrip()
            if inp in cMap.keys():
                cMap[inp]()
            else:
                break
        if (inp.isdigit()):
            inp = int(inp)
        return inp

    def display_search_results(self, results):
        # (Not finished yet)
        # arguments:
        # --> results: list of pids
        #
        # Return:
        # --> prints out product details in form |PID|NAME|UNIT|NUM_OF_STORES|
        count = 0
        #FUCKproduct_details(product_id)
        for prod in results:
            print(prod)
            pd = self.product_details(prod)
            # t1 layout: for each product (pid, name, unit, cat)
            # t2 layout: for each store (sid, name, uprice, qty, num_of_orders?)
            # t2 query doesnt fully work I dont think
            # doesnt give proper num of orders
            #t1, t2 = self.more_product_details(prod)
        #####if len(t2) > 0:             # only display products that are carried by a store
                                        # maybe check that store qty != 0 too
            if ((count % 5) == 0):
                if (count != 0):
                    more = get_input("Show more? y/n: ")
                    if (more == 'n'):
                        break
                print ("|PID|NAME|UNIT|NUM_OF_STORES|")

                '''
                For each matching product, list the product id, name, unit, the
                number of stores that carry it, the number of stores that have it
                in stock, the minimum price among the stores that carry it,
                the minimum price among the stores that have the product in stock,
                and the number of orders within the past 7 days.
                '''
                #print ("|{}|{}|{}|{}|".format(t1[0], t1[1], t1[2], len(t2)))
                # print(t1)
                # print(t2)
            print(pd)
            count += 1


    def ui_Home(self):
        print("Welcome to access.py, type --help for list of commands")
        print("press Enter key")
        raw_input()
        usr_inp = self.get_input("Type 1 to login, 0 to sign up: ")
        while (usr_inp not in [0, 1]):
            usr_inp = self.get_input("Type 1 to login, 0 to sign up: ")
        if (usr_inp == 0):
            # Create user
            self.create_account()
            return uiTest()
        elif (usr_inp == 1):
            # login
            verified = self.ui_Login()
            if (verified == False):
                print "Max attempts reached, please try again later!"
                raise SystemExit

            return verified
            #user_typ = verified[1]
            #username = verified[2]


def uiTest():
    a = access()

    while True:
        a.get_input("MP1: ")


if __name__ == "__main__":

    uiTest()
