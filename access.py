import sqlite3


class access:

    def __init__(self):

         self.conn = sqlite3.connect("./database.db") #connection to move database
         self.cursor = self.conn.cursor()


    def create_account(self, username, password, password_rpt, address):
        '''
        Checks if username exists in database. If it isn't, return false.
        Function returns true on success.
        '''
        username = username.lower()
        # if len(password < 8):
        #     return (False, "password must be 7 characters"
        # if

        self.cursor.execute("SELECT * FROM customers WHERE name=:usr;",{"usr": username})
        res=self.cursor.fetchall()

        if len(res) > 0:
            print "account already exists"
            return (False, "account already exists")



if __name__ == "__main__":
    a = access()
    a.create_account("Niho", "45673", "45673", "2005 Hilliard Place NW")
