import sqlite3
from datetime import datetime

class customer:

    '''
    module responsible for customer orders, cart etc..
    '''

    def __init__(self, customer):

        self.name=customer
        self.conn = sqlite3.connect("./database.db") #connection to move database
        self.cursor = self.conn.cursor()
        # We shouldnt need to re-verify user --> already verified
        SQL = "SELECT * FROM customers cust WHERE cust.name='{}'".format(customer)
        self.cursor.execute(SQL)
        result=self.cursor.fetchone()
        # if result != None:
        #     self.id=result[0]
        #     self.address=result[2]
        #     self.password=result[3]
        #     #Cart is a dictionary where keys are pid+'*'+sid and value the quantity
        #     self.cart=dict()
        #     print "Success! Welcome - {}".format(customer)
        # else:
        #     print "WARNING - customer does not exist"
        self.id = result[0]
        self.address = result[2]
        self.cart=dict()

    def show_cart(self, detailed = False):
        # also return keys so I can Index them in access.py
        count = 0
        keys = []

        for key in self.cart:
            keys.append(key)
            moreInfo = (self.cart)[key]
            qty = moreInfo[0]
            ppu = moreInfo[1]
            cst = moreInfo[2]
            #print(moreInfoc)
            if detailed == True:
                print("ITEM NUMBER ({}) ---- PID*SID: {} ---- QTY: {} ---- PPU: {} ---- TOTAL COST: {}".format(count, key, qty, ppu, cst))
            else:
                print("ITEM NUMBER ({}) ---- {}: ".format(count, key))

            count += 1
        return keys




    def add_to_cart(self, product_id, store_id, qty):

        '''
        Fuction takes in a product id and store id and adds product to cart.
        Function will return false if the qty ordered exceeds quantity in stock.
        Returns true otherwise

        Args: product_id (str), store_id (int), qty (int)
        Returns: success (boolean)
        '''
        success=True
        cart_key=product_id+'*'+str(store_id)

        SQL="SELECT crr.uprice, crr.qty FROM carries crr WHERE crr.pid='{}' AND crr.sid='{}';".format(product_id, store_id)
        self.cursor.execute(SQL)
        result=self.cursor.fetchone()
        if result == None:
            print "product {} does not exist in store {}".format(product_id, store_id)
            return False
        if qty > result[1]:
            print "quantity exceeds availability"
            success=False
        if cart_key in self.cart:
            self.cart[cart_key][0]+=qty
            self.cart[cart_key][1]=result[0]
            self.cart[cart_key][2]=self.cart[cart_key][0]*result[0]
        else:
            self.cart[cart_key]=[qty, result[0], qty*result[0]]
        return success


    def delete_from_cart(self, product_id, store_id, qty, ALL=False):

        '''
        Function takes a product and the store it is from and removes amount
        defined by quantity in the cart. If Var arg ALL is set to true, it will
        automatically remove the item completely from the cart

        Args: product_id (str), store_id (int), qty (int)
        Returns: success (boolean)
        '''
        cart_key=product_id+'*'+str(store_id)
        if cart_key not in self.cart:
            print "ERROR"
            return False
        else:
            if qty>=self.cart[cart_key][0] or ALL:
                self.cart.pop(cart_key)
                print "item completely removed from cart"
            else:
                self.cart[cart_key][0]-=qty
                self.cart[cart_key][2]=(self.cart[cart_key][0]*self.cart[cart_key][1])
                #print "{} item(s) removed from cart".format(qty)
            return True


    def get_cart_total(self):

        '''
        Returns the total value of the items in cart

        Args: None
        Returns: cart value (float)
        '''
        total = 0
        for x in self.cart.values():
            total+=x[2]
        return total


    def place_order(self):

        '''
        Function checks the validity for ALL items in our cart. If it happens that
        any quantity in cart exceeds the qty available at the time of ordering,
        function returns false. If success, function returns true as well as the
        order total

        Args: None
        Returns: (success (boolean), total (int))
        '''
        total = 0
        for k in self.cart.keys():
            data=self.cart[k]
            ps_id=k.split('*')
            SQL = "SELECT * FROM carries crr WHERE crr.pid='{}' AND crr.sid={} AND crr.qty>={};".format(ps_id[0], ps_id[1], data[0])
            self.cursor.execute(SQL)
            result=self.cursor.fetchone()
            if result == None:
                print "quantity exceeds availability"
                return (False, 0)
            else:
                self.cart[k][1]=result[-1]  #we need the most current price
                total+=result[-1]*data[0]
        return (True, total)


    def confirm_order(self):

        '''
        Function places an order for ALL items in our cart. If it happens that
        any quantity in cart exceeds the qty available at the time of ordering,
        function returns false. If success, a unique order id is genereated, and
        is added to customers order history as well as added to olines and orders
        in database. Cart will also be cleared on success

        Args: None
        Returns: (success (boolean), order_id (int))
        '''

        success = self.place_order()
        if not success[0]:
            print "Failed"
            return (False, 0)
        else:
            print "success"
            SQL = "SELECT MAX(oid) FROM orders;"
            self.cursor.execute(SQL)
            order_id = self.cursor.fetchone()[0]+1
            self.cursor.execute("INSERT INTO orders (oid, cid, odate, address) \
            VALUES (?, ?, ?, ?);", (order_id, self.id, datetime.today().strftime('%Y-%m-%d'), self.address))
            for k in self.cart.keys():
                #print self.cart
                data=self.cart[k]
                ps_id=k.split('*')
                #update quatnity in carries
                self.cursor.execute("UPDATE carries SET qty=qty-? WHERE pid=? AND sid=?;", (data[0], ps_id[0], ps_id[1]))
                #add new olines to ord
                self.cursor.execute("INSERT INTO olines (oid, sid, pid, qty, uprice) \
                VALUES (?, ?, ?, ?, ?);", (order_id, ps_id[1], ps_id[0], data[0], data[1]))
            #reset the cart and commit changes
            self.conn.commit()
            self.cart=dict()
            print "order successful"
            return (True, order_id)


    def order_history(self):

        '''
        Function retrieves order history according to the following specification

        listing should include for each order, the order id, order date, the number
        of products ordered and the total price; the orders should be listed in a
        sorted order with more recent orders listed first.

        Args: None
        Returns: list of rows (list (tuple))
        '''
        SQL="SELECT ord.oid, ord.odate, COUNT(DISTINCT(oln.pid)), SUM(oln.uprice*oln.qty) \
        FROM orders ord, olines oln ON ord.oid=oln.oid WHERE ord.cid='{}' GROUP BY ord.oid \
        ORDER BY ord.odate DESC;".format(self.id)
        self.cursor.execute(SQL)
        return self.cursor.fetchall()


    def order_detail(self, order_id):   #NOTE our database is kinda messed

        '''
        Function returns the details of a given order (order) id returns info
        that meets the following specification

        Details should include delivery information such as tracking number, pick up
        and drop off times, the address to be delivered, and a listing of the
        products in the order, which will include for each product the store id,
        the store name, the product id, the product name, quantity, unit and
        unit price

        Args: order_id (int)
        Returns: detail (tuple), product_detail (list)(tuple)
        '''
        #tracking number, pick up and drop off times, the address to be delivered
        SQL="SELECT dlr.trackingNo, dlr.pickUpTime, IFNULL(dlr.dropOffTime, 'NA'), ord.address \
        FROM orders ord, deliveries dlr ON ord.oid=dlr.oid WHERE ord.oid={};".format(order_id)
        self.cursor.execute(SQL)
        detail=self.cursor.fetchone()

        #listing of the products in the order, which will include for each product the store id,
        #the store name, the product id, the product name, quantity, unit and unit price
        SQL="SELECT str.sid, str.name, oln.pid, prd.name, oln.qty, prd.unit, oln.uprice \
        FROM orders ord, olines oln, stores str, products prd ON ord.oid=oln.oid \
        AND  oln.sid=str.sid AND prd.pid=oln.pid WHERE ord.oid={};".format(order_id)
        self.cursor.execute(SQL)
        product_detail=self.cursor.fetchall()
        return (detail, product_detail)



#if __name__ == "__main__":
    #c=customer("davood")
