import sqlite3

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
            self.order=list()
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

        SQL="SELECT qty FROM carries"
        print SQL
        self.cursor.execute(SQL)
        result=self.cursor.fetchone()
        print result
        # if result == None:
        #     print "product {} does not exist in store {}".format(product_id, store_id)
        #     return False
        # if qty >= result[0]:
        #     print "quantity exceeds availability"
        #     success=False
        # if cart_key in self.cart:
        #     self.cart[cart_key]+=qty
        # else:
        #     self.cart[cart_key]=qty
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
                self.cart[cart_key]-=qty
                print "{} item(s) removed from cart".format(qty)
            return True

    def place_order(self):

        '''
        Function places an order for ALL items in our cart. If it happens that
        any quantity in cart exceeds the qty available at the time of ordering,
        function returns false. If success, a unique order id is genereated, and
        is added to customers order history as well as added to olines and orders
        in database. Cart will also be cleared on success

        Args: None
        Returns: success (boolean)
        '''


        pass


if __name__ == "__main__":
    c=customer("davood")
    c.add_to_cart('p20', 20, 100)
    #c.delete_from_cart("p10", 20, 87)
    print c.cart
