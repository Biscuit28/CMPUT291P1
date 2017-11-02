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
        SQL = "SELECT * FROM customers cust WHERE cust.name='{}'".format(customer)
        self.cursor.execute(SQL)
        result=self.cursor.fetchone()
        if result != None:
            self.id=result[0]
            self.address=result[2]
            self.password=result[3]
            #Cart is a dictionary where keys are pid+'*'+sid and value the quantity
            self.cart=dict()
            print "Success! Welcome - {}".format(customer)
        else:
            print "WARNING - customer does not exist"


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
            self.cart[cart_key][2]=qty*result[0]
        else:
            self.cart[cart_key]=[qty, result[0], qty*result[0]]
        return success


    def delete_from_cart(self, product_id, store_id, qty, ALL=False):

        '''
        Function takes a product and the store it is from and removes amount
        defined by quantity in the cart. If Var arg all is set to true, it will
        automatically remove the item completely from the cart

        Args: product_id (str), store_id (int), qty (int)
        Returns: success (boolean)
        '''
        cart_key=product_id+'*'+str(store_id)
        if cart_key not in self.cart:
            print "product and store combo does not exist in cart"
            return False
        else:
            if qty>=self.cart[cart_key] or ALL:
                self.cart.pop(cart_key)
                print "item completely removed from cart"
            else:
                self.cart[cart_key][0]-=qty
                self.cart[cart_key][2]=(self.cart[cart_key][0]*self.cart[cart_key][1])
                print "{} item(s) removed from cart".format(qty)
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
                print c.cart
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



if __name__ == "__main__":
    c=customer("davood")
    c.add_to_cart("p1", 2, 100)
    c.add_to_cart("p3", 1, 10)
    print c.cart
    print c.confirm_order()
