import sqlite3
from datetime import datetime


class agent:

    '''
    Module responsible for all agent activities
    '''

    def __init__(self, agent):

        self.name=agent
        self.conn = sqlite3.connect("./database.db") #connection to move database
        self.cursor = self.conn.cursor()
        SQL = "SELECT * FROM agents agt WHERE agt.name='{}'".format(agent)
        self.cursor.execute(SQL)
        result=self.cursor.fetchone()
        if result != None:
            self.id=result[0]
            self.password=result[2]
            print "Success! Welcome - {}".format(agent)
        else:
            print "WARNING - agent {} does not exist".format(agent)


    def view_orders(self):

        '''
        Function returns orders and deliveries for the agent

        Args: None
        Returns: (t1 (list)(tuple), t2 (list)(tuple))
        '''
        # SQL="SELECT * FROM orders;"
        # self.cursor.execute(SQL)
        # t1=self.cursor.fetchall()
        #
        # SQL="SELECT * FROM deliveries;"
        # self.cursor.execute(SQL)
        # t2=self.cursor.fetchall()

        SQL="SELECT oid FROM orders;"
        self.cursor.execute(SQL)
        t1=self.cursor.fetchall()

        SQL="SELECT oid FROM deliveries;"
        self.cursor.execute(SQL)
        t2=self.cursor.fetchall()

        return (t1, t2)


    def view_carries(self):

        '''
        Function returns the carries table

        Args: None
        Returns: carries (list)(tuple)
        '''
        SQL="SELECT * FROM carries;"
        self.cursor.execute(SQL)
        return self.cursor.fetchall()


    def set_delivery(self, orders, pickUpTime=None):

        '''
        Function allows agent to schedule a delivery by passing a list of orders
        that the delivery will include, and a optional pickUpTime that is set
        by default to None. Function will autoamtically generate unique tracking
        id

        Args: orders (list), pickUpTime(varArg date)
        Returns: success (boolean)
        '''
        self.cursor.execute("SELECT MAX(trackingNo) FROM deliveries;")
        maxtrack=self.cursor.fetchone()
        trackingNo=maxtrack[0]+1
        for oid in orders:
            #oid = oid[0]
            pickUpTime = raw_input("-->--> PICK UP TIME FOR ORDER {} (press enter for DEFAULT): ".format(oid)).strip() or None

            # self.cursor.execute("INSERT INTO deliveries (trackingNo, oid, pickUpTime, dropOffTime) \
            # VALUES (?, ?, ?, ?);", (trackingNo, oid, pickUpTime, None))
            self.cursor.execute("INSERT INTO deliveries VALUES (?, ?, ?, ?);", (trackingNo, oid, pickUpTime, None))
        self.conn.commit()
        return True


    def view_delivery(self, trackingNo):

        '''
        Function allows agents to view delivery details through trackingNo. Returns
        rows of the details of the delivery.

        Args: trackingNo (int)
        Returns: list of rows (list)(tuples)
        '''
        SQL="SELECT trackingNo, oid, IFNULL(pickUpTime, 'NA'), IFNULL(dropOffTime, 'NA') \
        FROM deliveries WHERE trackingNo={}".format(trackingNo)
        self.cursor.execute(SQL)
        return self.cursor.fetchall()


    def edit_delivery_order_time(self, trackingNo, oid, pickUpTime=None, dropOffTime=None):

        '''
        Function allows agent to able to pick up an order and update the pick up time
        and/or the drop off time. Function returns true upon success

        Args: trackingNo(int), oid(int), pickupTime(datetime), dropOffTime(datetime)
        Returns: success (boolean)
        '''
        if pickUpTime == None and dropOffTime == None:
            print "cannot update empty values"
            return False
        elif pickUpTime != None and dropOffTime != None:
            self.cursor.execute("UPDATE deliveries SET pickUpTime=?, dropOffTime=? \
            WHERE trackingNo=? AND oid=?;", (pickUpTime, dropOffTime, trackingNo, oid))
        elif pickUpTime != None:
            self.cursor.execute("UPDATE deliveries SET pickUpTime=? WHERE trackingNo=? \
            AND oid=?;", (pickUpTime, trackingNo, oid))
        else:
            self.cursor.execute("UPDATE deliveries SET dropOffTime=? WHERE trackingNo=? \
            AND oid=?;", (dropOffTime, trackingNo, oid))
        self.conn.commit()
        return True


    def remove_order_from_delivery(self, trackingNo, oid):

        '''
        Fucntion allows agent to remove an order from a delivery by specifying
        a trackingNo and oid. Returns true on success

        Args: trackingNo (int), oid (int)
        Returns: success (boolean)
        '''
        SQL="DELETE FROM deliveries WHERE trackingNo={} AND oid={}".format(trackingNo, oid)
        self.cursor.execute(SQL)
        self.conn.commit()
        return True


    def update_stock(self, product_id, store_id, qty=None, uprice=None):

        '''
        Function allows agent to add to stock of a specific product in a
        specific store as well as change the price

        Args: product_id (str), store_id (int), qty (int), uprice (float)
        Returns: success (boolean)
        '''
        if qty == None and uprice == None:
            print "cannot update empty values"
            return False
        elif qty != None and uprice != None:
            self.cursor.execute("UPDATE carries SET qty=qty+?, uprice=? \
            WHERE pid=? AND sid=?;", (qty, uprice, product_id, store_id))
        elif qty != None:
            self.cursor.execute("UPDATE carries SET qty=qty+? \
            WHERE pid=? AND sid=?;", (qty, product_id, store_id))
        else:
            self.cursor.execute("UPDATE carries SET uprice=? \
            WHERE pid=? AND sid=?;", (uprice, product_id, store_id))
        self.conn.commit()
        return True




# if __name__ =="__main__":
#     a=agent("Joshua")
#     a.update_stock("p3", 1)
