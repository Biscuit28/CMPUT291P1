import sqlite3
import sys
import access
import getpass
from customer import customer
from agent import agent
from collections import defaultdict
import time

#global AGENT
#global CUSTOMER

class access:
    '''
    module responsible for login/signup and general search
    '''

    def __init__(self):

         self.conn = sqlite3.connect("./database.db") #connection to move database
         self.cursor = self.conn.cursor()
         self.user_typ = -1
         self.user = None


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
            # try:
            #     CUSTOMER
            # except:
            #     CUSTOMER = customer(username)
        elif user_typ == 0:
            self.cursor.execute("SELECT * FROM agents WHERE name=? AND pwd=?", (username, password))
            # try:
            #     AGENT
            # except:
            #     AGENT = agent(username)

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
        #    a list which follows the indexing [0, 1, 2, 3, 5, 4, 6, 7] using guide above
        #    there is no god
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
        q4="SELECT SUM(oln.qty) AS tot FROM olines oln, orders ord ON oln.oid=ord.oid \
        WHERE oln.pid='{}' AND 7>=JULIANDAY('now')-JULIANDAY(ord.odate) GROUP BY oln.sid".format(product_id)

        queries = [q1, q2, q3, q4]
        for q in queries:
            self.cursor.execute(q)
            qr = self.cursor.fetchone() # should work as fetch one aswell

            if qr == None:
                if q != q4:
                    pd.append(0)
                    pd.append(None)
                else:
                    pd.append(0)

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
        print("------------------- LOGIN ---------------------")
        print("")
        while (True):
            #user_typ = input("Type 1 for customer login or 0 for agent login: ")
            #print("Type 1 for customer login or 0 for agent login: ")
            #user_typ = self.get_input("Type 1 for customer login or 0 for agent login: ")
            user_typ = self.get_input("Type 1 for customer login or 0 for agent login: ")
            if (user_typ in [0,1]):
                break
        print("")
        for attempt in range(3):
            # Use Raw input here (dont use get_input function)
            print("Login Attempts Remaining: [{}]".format(2-attempt))
            username = str(raw_input("-->Username: ").lower()).rstrip()
            #password = str(raw_input("-->Password: "))
            password = getpass.getpass("-->Password: ")
            verified = self.login(user_typ, username, password)[0]
            print("")
            if (verified):
                #print("")
                return (True, user_typ, username)
            #print("")

        return False

    def inp_help(self):
        print("---------------- HELP MENU --------------------")
        print("")
        print("commands can be used on any line that does not have an arrow (-->)")
        universal = ["--help", "--quit", "--login", "--logout", "--signup"]
        cu_coms = ["--search", "--cart"]
        ag_coms = ["--admin"]

        for command in universal:
            print(command)

        if self.user_typ == 1:
            print("")


            for cu_com in cu_coms:
                print(cu_com)

        if self.user_typ == 0:
            print("")
            print("<<<<AGENT COMMANDS>>>>")
            for ag_com in ag_coms:
                print(ag_com)

        print("")

    def inp_quit(self):

        if (self.user_typ != -1):
            self.inp_logout()
            print "logging out..."
            for i in range(3):
                print "|/\/\/\/\/\/\/\/|"
                time.sleep(0.1)
                print "|\/\/\/\/\/\/\/\|"
                time.sleep(0.1)



        print("-----------------------------------------------")
        print("Have nice day!")
        print("-----------------------------------------------")
        print("")
        print("")
        raise SystemExit

    def inp_search(self):
        # if user is customer

        if (self.user_typ == 1):
            #print("-----------------------------------------------")
            searchInput = self.get_input(">>>>>>>Searchbar: ")
            #print("-----------------------------------------------")

            searchInput = searchInput.split()
            r= self.search(searchInput)
            if len(r) != 0:
                print("")
                self.display_search_results(r)
            else:
                print("No Match Results Found!")
        else:
            print ("Please log in as customer to use search feature.")

    def inp_login(self):
        # login
        if (self.user_typ != -1):
            print("Please logout first with --logout")
            return
        verified = self.ui_Login()
        if (verified == False):
            print "Max attempts reached, please try again later!"
            raise SystemExit
        self.user_typ = verified[1]
        if self.user_typ == 1:
                #CUSTOMER = customer(verified[2])
                self.user = customer(verified[2])
        elif self.user_typ == 0:
                #AGENT = agent(verified[2])
                self.user = agent(verified[2])
        return verified

    def inp_logout(self):
        if self.user_typ == -1:
            print("NOT LOGGED IN")
        else:
            self.user_typ = -1
        # wipe
        # CUSTOMER = None
        # AGENT = None
            self.user = None
        #return uiTest()

    def inp_signup(self):

        if (self.user_typ != -1):
            print ("Please logout before making new account")

        else:
            self.create_account()
            return uiTest()

    def inp_cartDetails(self):
        # if not customer
        if (self.user_typ != 1):
            return
        options = ['b', '0', '1', '2', '3', 'p', 'h']
        # cart_keys = ((self.user).cart).keys()
        # num_items = len(cart_keys)
        # print("CART: ")
        # CUSTOMER.cart
        # print("CART TOTAL")
        # CUSTOMER.get_cart_total()

        print("------------------ CART VIEW ------------------")
        print("<<<OPTIONS>>>")
        print("GO BACK --------- TYPE b --")
        print("SEE CART--------- TYPE 0 --")
        print("SEE CART TOTAL--- TYPE 1 --")
        print("ADJUST QUANTITY-- TYPE 2 --")
        print("DEL FROM CART---- TYPE 3 --")
        print("PLACE ORDER------ TYPE p --")
        print("ODER HISTORY----- TYPE h --")
        #print("")

        while True:
            print("")
            cart_keys = ((self.user).cart).keys()
            num_items = len(cart_keys)

            inp = None
            while inp not in options:
                inp = raw_input("-->Type Option: ")

            if (inp == 'b'):
                print("---------------- END CART VIEW ----------------")
                print("")
                return

            if (inp == '0'):
                print("CART: ")
                self.user.show_cart(detailed = True)
                #print(((self.user).cart).keys())
            if (inp == '1'):
                print("CART TOTAL")
                total = (self.user).get_cart_total()
                print("${}".format(total))

            if (inp == '2'):
                #inp = raw_input("-->Type : ")
                # delete_from_cart(self, product_id, store_id, qty, ALL=False)
                keys = self.user.show_cart()
                k_inp = int(raw_input("-->-->ENTER ITEM NUMBER: "))
                if (k_inp < len(keys)):
                    key = keys[k_inp]
                    key = key.split("*")
                    pid = key[0]
                    sid = key[1]
                    qty = int(raw_input("-->-->Type QTY you wish to add (+ or - integer): "))
                    qty = -1 * qty
                    # pid = raw_input("-->Type PID of item to delete --------: ")
                    # sid = int(raw_input("-->Type SID of store to delete from --: "))
                    # qty = int(raw_input("-->Type QTY you wish to delete --: "))
                    (self.user).delete_from_cart(pid, sid, qty, ALL=False)
                else:
                    print("ITEM NUMBER {} DOES NOT EXIST!".format(k_inp))

            if (inp == '3'):
                #inp = raw_input("-->Type : ")
                # delete_from_cart(self, product_id, store_id, qty, ALL=False)
                print("\nITEMS IN CART")
                keys = self.user.show_cart()
                k_inp = int(raw_input("\n-->-->ENTER ITEM NUMBER TO DELETE: "))
                if (k_inp < len(keys)):
                    key = keys[k_inp]
                    key = key.split("*")
                    pid = key[0]
                    sid = key[1]
                    # pid = raw_input("-->Type PID of item to delete --------: ")
                    # sid = int(raw_input("-->Type SID of store to delete from --: "))
                    # qty = int(raw_input("-->Type QTY you wish to delete --: "))
                    (self.user).delete_from_cart(pid, sid, 0, ALL=True)
                else:
                    print("ITEM NUMBER {} DOES NOT EXIST!".format(k_inp))
                # pid = raw_input("-->Type PID of item to delete --------: ")
                # sid = int(raw_input("-->Type SID of store to delete from --: "))
                # (self.user).delete_from_cart(pid, sid, 0, ALL=True)

            if (inp == 'p'):
                (self.user).confirm_order()
            if (inp == 'h'):
                history = (self.user).order_history()
                for order in history:
                    print(order)

    def inp_adminFunctions(self):

        if (self.user_typ != 0):
            print("here")
            return

        options = ['S', 'U', 'A', 'B']

        print("")
        print("------------------- ADMIN ---------------------")
        print("LOGGED IN AS AGENT: {}".format((self.user).name))
        print("-----------------------------------------------")
        print("")
        print("<<<<<<<<<<<OPTIONS>>>>>>>>>>>")
        print(">GO BACK----------------- TYPE B --")
        print(">SET DELIVERY------------ TYPE S ---")
        print(">UPDATE DELIVERY--------- TYPE U ---")
        print(">ADD TO STOCK------------ TYPE A ---")

        while True:
            print("")
            # cart_keys = ((self.user).cart).keys()
            # num_items = len(cart_keys)

            inp = None
            while inp not in options:
                inp = raw_input("-->Type Option: ")

            if (inp == 'B'):
                print("---------------- END ADMIN VIEW ----------------")
                print("")
                return

            if (inp == 'A'):
                # Add to stock
                pid = raw_input("-->--> PID: ")
                sid = int(raw_input("-->--> SID: "))

                # Check that pid and sid that agent typed is exists
                SQL="SELECT crr.uprice, crr.qty FROM carries crr WHERE crr.pid='{}' AND crr.sid='{}';".format(pid, sid)
                self.cursor.execute(SQL)
                result=self.cursor.fetchone()
                if result == None:
                    print "-->-->PRODUCT {} DOES NOT EXIT IN STORE {}".format(pid, sid)

                else:
                    try:
                        qty = int(raw_input("-->--> ADD QTY (press enter to skip): "))
                    except ValueError:
                        qty = None
                    try:
                        uprice = float(raw_input("-->--> NEW PRICE (press enter to skip): "))
                    except ValueError:
                        uprice = None

                    update = (self.user).update_stock(pid, sid, qty, uprice)
                    if update == True:
                        print("STOCK UPDATE ---- SUCCESSFUL")
                    else:
                        print("STOCK UPDATE ---- NOT SUCCESSFUL")


            if (inp == 'S'):
                # Set delivery
                all_orders, deliv_orders = (self.user).view_orders()
                #print(orders)
                #print(deliveries)
                orders = []
                for o in all_orders:
                    if o not in deliv_orders:
                        orders.append(o[0])
                # print("orders needing delivery")
                # for order in orders:
                #     print(order[0])

                #pickUpTime = raw_input("-->--> PICK UP TIME (press enter for DEFAULT): ").strip() or None
                count = 0
                print("")
                print(">>>>ORDERS NOT IN DELIVERY>>>>")
                for order in orders:
                    print("ORDER ({}) ---- OID: {}".format(count, order))
                    count += 1

                print("")
                print(">>>>TYPE A SPACE SEPARATED STRING OF OID's TO ADD TO A DELIVERY, OR PRESS ENTER TO GO BACK")
                usr_inp = raw_input("-->--> OID STRING: ")
                test = usr_inp.strip() or None
                if (test != None):
                    usr_inp = usr_inp.split()

                    try:
                        usr_inp = map(int, usr_inp)     # conver input string to list of ints
                    except ValueError:
                        print("ERROR: RETURNING TO HOME")
                        return


                    # CHECK that every input is valid
                    flag = True
                    for inp in usr_inp:
                        inp = int(inp)
                        if inp not in orders:
                            print("INVALID: OID {} IS NOT IN ORDERS!".format(inp))
                            flag = False

                    if flag:
                        success = (self.user).set_delivery(usr_inp, pickUpTime=None)
                        if (success):
                            print("DELIVERY SETUP ---- SUCCESSFUL")
                        else:
                            print("DELIVERY SETUP ---- NOT SUCCESSFUL")

            if (inp == 'U'):
                # Update delivery
                oids = []
                print("")
                print(">>>>UPDATE DELIVERY>>>>")
                print("")
                try :
                    trackingNo = int(raw_input("-->--> ENTER 'trackingNo': "))
                except ValueError:
                    print("ERROR: RETURNING TO HOME")
                    return

                count = 0
                r = (self.user).view_delivery(trackingNo)
                for order in r:
                    oids.append(order[1])
                    print("> INDEX ({}) ---- OID: {}".format(count, oids[count]))
                    count += 1

                print("")

                try :
                    index = int(raw_input("-->--> ENTER INDEX OF OID TO EDIT: "))
                except ValueError:
                    print("ERROR: RETURNING TO HOME")
                    return

                if index >= len(oids):
                    print("INVALID: INDEX OUR OF RANGE!")
                    return


                pickUpTime = raw_input("-->--> ENTER NEW 'pickUpTime', PRESS ENTER FOR DEFAULT: ")
                pickUpTime = pickUpTime.strip() or None

                dropOffTime = raw_input("-->--> ENTER NEW 'dropOffTime', PRESS ENTER FOR DEFAULT: ")
                dropOffTime = dropOffTime.strip() or None

                (self.user).edit_delivery_order_time(trackingNo, oids[index], pickUpTime, dropOffTime)





    def get_input(self, message):
        # Function to use when getting input from user
        # checks is input is a command from user, if not, return output as is
        # output will always be string so if we want to return other type, must check and change (eg int)
        #cMap = {"--help":self.inp_help, "--quit":self.inp_quit, "--logout":self.inp_logout}
        cMap = {"--help":self.inp_help, "--quit":self.inp_quit, "--search":self.inp_search, "--login":self.inp_login, "--logout":self.inp_logout, "--signup":self.inp_signup, "--cart":self.inp_cartDetails, "--admin":self.inp_adminFunctions}
        while True:
            inp = raw_input(message).rstrip().lower()
            if inp in cMap.keys():
                cMap[inp]()
            else:
                break
        if (inp.isdigit()):
            inp = int(inp)
        return inp

    def display_more_details(self, pid):
        t1, t2 = self.more_product_details(pid)
        count = 0
        print("|PID|NAME|UNIT|CATEGORY|")
        print("|{}|{}|{}|{}|".format(*t1[0]))
        if (len(t2) > 0):
            print("\n|SID|STORE NAME|LOWEST PRICE|QUANTITY IN STOCK|ORDERS IN LAST 7 DAYS|")
            for store in t2:
                #print(store)
                print("STORE NUMBER ({}) ---- |{}|{}|{}|{}|{}|".format(count, *store))
                count += 1
        return t2


    def display_search_results(self, results):
        print("--------------- SEARCH RESULTS ----------------")

        # (Not finished yet)
        # arguments:
        # --> results: list of pids
        #
        # Return:
        # --> prints out product details in form |PID|NAME|UNIT|NUM_OF_STORES|
        count = 0
        #product_details(product_id)
        print(results)
        for prod in results:
            #print(prod)
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
                print ("|PID|NAME|UNIT|NUM_OF_STORES|MIN_PRICE|IN_STOCK|MIN_PRICE_IS|LAST 7 DAYS")

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
            print("ITEM NUMBER ({}) ---- |{}|{}|{}|{}|{}|{}|{}|{}|".format(count, *pd))
            #print(pd)
            count += 1

        user_inp = self.get_input("\nWould you like to see more details on an item listed? y/n: ")
        while user_inp not in ['y', 'n']:
            user_inp = self.get_input("Would you like to see more details on items listed? y/n: ")

        if user_inp == 'y':
        #####pid = self.get_input("Enter PID of item: ")
            item_n = self.get_input("Enter ITEM NUMBER of item: ")
            # Returns: (product detial (list), store info (list))
            pid = results[item_n]
            print("")
            print("-----------------------------------------------")
            print("------------------ MORE INFO ------------------")
            t2 = self.display_more_details(pid)
            #t1, t2 = self.display_more_details(pid)
            # t1, t2 = self.more_product_details(pid)
            # print(t1)
            # print(t2)

            # Add to cart option
            # if (pd[5] == 0):
            #     print("Sorry, no store carries this product.")
            #     return
            user_inp = self.get_input("\nWould you like to add item to cart? y/n: ")
            while user_inp not in ['y', 'n']:
                user_inp = self.get_input("Would you like to add item to cart? y/n: ")

            if user_inp == 'y':
                #if (pd[5] == 0):
                if (len(t2) == 0):
                    print("Sorry, no store has this product in stock.")
                    print("")
                    return
                # add_to_cart(self, product_id, store_id, qty)
                # pid = raw_input("-->Enter PID of item: ")
                # sid = int(raw_input("-->Enter SID of store: "))

                # pid has not changes --> leave
                # sid --> picked by user
                s_num = int(raw_input("-->Enter STORE NUMBER of store to order from: "))
                sid = t2[s_num][0]
                #qty = int(raw_input("-->Enter QTY of item: "))
                qty = 1 # DEFAULT IS 1
                (self.user).add_to_cart(pid, sid, qty)
                print("")




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
    # global USERNAME
    # global AGENT
    # global CUSTOMER
    #CUSTOMER = None
    print("-----------------------------------------------")
    print("-Mini Project 1--------------------------V1.0--")
    print("-----------------------------------------------")
    print("")
    while True:
        a.get_input("MP1: ")
        #print(a.user)

if __name__ == "__main__":

    uiTest()
