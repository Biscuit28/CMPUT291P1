from access import access
from customer import customer
from agent import agent
import time
from datetime import datetime

def interface():
    state = "main menu"

    '''
    mainmenu ___userlogin/signup menu_______________login success menu_________productsearch
            |
            |___agentlogin
    '''
    global USERNAME
    global AGENT
    global CUSTOMER

    while True:

        if state=="main menu":
            while True:
                inp = raw_input("Hello! Please enter '1' for customer, and '0' for agent: ")
                if inp=="1":
                    state="user login/signup menu"
                    break
                elif inp=="0":
                    state="agent login" #NOTE not complete
                    break
                else:
                    continue

        if state=="user login/signup menu":
            a=access()
            brk=False
            while True:
                print "Please enter '0' to login, '1' to signup! or '2' to go back"
                inp = raw_input("your input: ")
                if inp=='0':
                    while True:
                        proceed = raw_input("press any key to proceed, or 'b' to go back: ")
                        if proceed=='b':
                            break
                        usrname = raw_input("username: ")
                        password = raw_input("password: ")
                        success = a.login(usrname, password)
                        if success[0]:
                            USERNAME=usrname
                            state="login success menu"
                            brk=True
                            break
                        else:
                            continue
                if inp=='1':
                    while True:
                        proceed = raw_input("Sign up menu, press any key to proceed, or 'b' to go back: ")
                        if proceed=='b':
                            break
                        usrname=raw_input("Enter a username (must be 4 char long at least): ")
                        pw=raw_input("Enter a password (must be at least 8 characters long): ")
                        pwr=raw_input("Please repeat above password: ")
                        addr=raw_input("Please Enter a valid address: ")
                        conf=raw_input("are you satisfied with the info above (Y/N)?: ").lower()
                        if conf=="y":
                            success=a.create_account(usrname, pw, pwr, addr)
                            if success[0]:
                                USERNAME=usrname
                                state="login success menu"
                                brk=True
                                break
                            else:
                                continue
                        else:
                            continue

                if inp=='2':
                    state="main menu"
                    break
                if brk:
                    break

        if state=="login success menu":
            try:
                CUSTOMER
            except:
                CUSTOMER = customer(USERNAME)
            while True:
                print "to search for a product press '0', to go to basket press '1' to view order history press '2' to go logout press 'Q'"
                inp=raw_input("your input: ").lower()
                if inp=='0':
                    state="product search"
                    break
                elif inp=='1':
                    state="basket view" #NOTE not complete
                    break
                elif inp=='2':
                    state="view order history"
                    break
                elif inp=='q':
                    state="main menu"
                    break

        if state=="product search":
            a=access()
            while True:
                inp=raw_input("Search for a product or press 'b' to go back: ")
                if inp=='b':
                    state="login success menu"
                    break
                inps = inp.split()
                result=a.search(inps)
                result=a.get_products(result)
                MAXLEN = len(result)-1
                print "found {} matching results for {}".format(len(result), inp)
                #logic for implementing displaying 5 items at a time
                start=0
                end=5
                while True:
                    if (end > MAXLEN):
                        end = MAXLEN+1
                    counter = start
                    for i in range(start,end):
                        print counter, result[i]
                        counter+=1
                    counter=start
                    print "displaying {}/{} items. \nEnter 'M' to view more \nEnter a index of the product you want to view details\nEnter 'b' to go back ".format(end, MAXLEN+1)
                    inp=raw_input("Your Input: ").lower()
                    if inp=='m':
                        start=end
                        end+=5
                    if inp=='b':
                        break
                    try:
                        inp=int(inp)
                        print 'success'
                    except:
                        continue
                    if inp>=0 and inp<=MAXLEN:
                        pid=result[inp][0]
                        result_details=a.product_details(pid)
                        print "Product details: "
                        if result_details[0]==None:
                            print "No stores carry this item at the moment"
                        else:
                            print result_details[0]
                        print "store details: "
                        if len(result[1])==0:
                            print "not carried by any stores"
                        else:
                            store_index = 0
                            for res in result_details[1]:
                                print store_index, res
                                store_index+=1
                            print "enter the index of the store you would like to buy from, or press any key to go back"
                            selection=raw_input("your input: ")
                            try:
                                selection=int(selection)
                                print 'success'
                            except:
                                continue
                            if selection >= 0 and selection < len(result[1]):
                                sid = result_details[1][selection][0]
                                outerbreak=False
                                while True:
                                    print "how many item would you like to add to basket or press 'b' to go back?"
                                    amt = raw_input("Your input: ")
                                    if amt=='b':
                                        break
                                    try:
                                        amt=int(amt)
                                    except:
                                        continue
                                    if amt <= 0:
                                        print "you cannot have 0 or less items in your cart. please change the quantity"
                                        continue
                                    ct=CUSTOMER.add_to_cart(pid, sid, amt)
                                    if ct:
                                        print 'items added to cart!'
                                        print CUSTOMER.cart
                                        break
                                    else:
                                        while True:
                                            print "quantity exceeds availability, would you like to change order amount (Y/N)?"
                                            changecart=raw_input("Your input: ").lower()
                                            if changecart=='y':
                                                CUSTOMER.delete_from_cart(pid, sid, 0, ALL=True)
                                                break
                                            if changecart=='n':
                                                outerbreak=True
                                                break
                                            else:
                                                print "please enter Y or N"
                            else:
                                print 'not a valid index'

        if state=="basket view":
            while True:
                counter = 0
                key_list=[]
                for k in CUSTOMER.cart.keys():
                    key_list.append(k)
                    print counter, CUSTOMER.cart[k]
                    counter+=1
                print 'TOTAL: ', CUSTOMER.get_cart_total()
                print "to edit basket, enter index, to order items, enter 'o', to go back enter 'b'"
                inp=raw_input("Your Input: ")
                if inp=='b':
                    state="login success menu"
                    break
                elif inp=='o':
                    if CUSTOMER.get_cart_total()==0:
                        print "you do not have anything in your cart!"
                    else:
                        while True:
                            print 'YOUR TOTAL', CUSTOMER.place_order()[1]
                            confirm=raw_input("confirm order? (Y/N): ").lower()
                            if confirm=='y':
                                ordercomplete=CUSTOMER.confirm_order()
                                if ordercomplete[0]:
                                    print 'Order successful!'
                                    print 'your order id --', ordercomplete[1]
                                    time.sleep(3)
                                    break
                                else:
                                    print 'Order unsuccessful, please check your cart'
                                    break
                            elif confirm=='n':
                                break
                            else:
                                continue
                try:
                    inp=int(inp)
                except:
                    continue
                if inp>=0 and inp<=counter:
                    mykey = key_list[inp].split('*')
                    pid=mykey[0]
                    sid=int(mykey[1])
                    while True:
                        print "to add to cart press 'a-DESIRED AMOUT'. to remove from cart, press 'r-DESIRED AMOUNT'. to go back press 'b'"
                        r=raw_input("Your Input: ").split('-')
                        print r
                        if r[0] == 'a':
                            try:
                                amt=int(r[1])
                            except:
                                break
                            if CUSTOMER.add_to_cart(pid, sid, amt):
                                print 'cart updated!'
                                break
                            else:
                                while True:
                                    print "quantity exceeds availability, would you like to change order amount (Y/N)?"
                                    changecart=raw_input("Your input: ").lower()
                                    if changecart=='y':
                                        CUSTOMER.delete_from_cart(pid, sid, 0, ALL=True)
                                        break
                                    if changecart=='n':
                                        break
                                    else:
                                        print "please enter Y or N"
                        if r[0] == 'r':
                            try:
                                amt=int(r[1])
                            except:
                                break
                            CUSTOMER.delete_from_cart(pid, sid, amt)
                            print 'cart updated'
                            break
                        if r[0]=='b':
                            break

        if state=="view order history":
            result=CUSTOMER.order_history()
            MAXLEN = len(result)-1
            start=0
            end=5
            while True:
                if (end > MAXLEN):
                    end = MAXLEN+1
                counter = start
                for i in range(start,end):
                    print counter, result[i]
                    counter+=1
                counter=start
                print "displaying {}/{} items. \nEnter 'M' to view more \nEnter a index of the order you want to view details\nEnter 'b' to go back ".format(end, MAXLEN+1)
                inp=raw_input("Your Input: ").lower()
                if inp=='m':
                    start=end
                    end+=5
                if inp=='b':
                    state="login success menu"
                    break
                try:
                    inp=int(inp)
                except:
                    continue
                if inp>=0 and inp<=MAXLEN:
                    oid=int(result[inp][0])
                    print oid
                    order_detail=CUSTOMER.order_detail(oid)
                    print "delivery info --"
                    dlrinfo=order_detail[0]
                    if dlrinfo == None:
                        print "delivery has not been scheduled by the agent yet"
                    else:
                        print dlrinfo
                    print "product info--"
                    for o in order_detail[1]:
                        print o
                    raw_input("press any key to go back")

        if state=="agent login":
            a=access()
            brk=False
            while True:
                print "Please enter '0' to login, 'b' to go back"
                inp = raw_input("your input: ")
                if inp=='0':
                    while True:
                        proceed = raw_input("press any key to proceed, or 'b' to go back")
                        if proceed=='b':
                            break
                        usrname = raw_input("username: ")
                        password = raw_input("password: ")
                        success = a.login(usrname, password, customer=False)
                        if success[0]:
                            USERNAME=usrname
                            state="agent login success menu"
                            brk=True
                            break
                        else:
                            continue
                if inp=='b':
                    state="main menu"
                    break
                if brk:
                    break

        if state=="agent login success menu":
            try:
                AGENT
            except:
                AGENT = agent(USERNAME)
            while True:
                print "to set up a delivery press '0', to update a delivery press '1' to Add to Stock press '2' to go logout press 'Q'"
                inp=raw_input("your input: ").lower()
                if inp=='0':
                    state="set up delivery"
                    break
                elif inp=='1':
                    state="update delivery"
                    break
                elif inp=='2':
                    state="add to stock"
                    break
                elif inp=='q':
                    state="main menu"
                    break

        if state=="set up delivery":
            print "----------------orders-------------------"
            res=AGENT.view_orders()
            for x in res[0]:
                print x
            print "--------------deliveries------------------"
            for i in res[1]:
                print i
            while True:
                print "Enter the order ids you wish to add to delivery or press 'b' to go back"
                inp=raw_input("Your input: ").lower()
                if inp=='b':
                    state="agent login success menu"
                    break
                if inp=='':
                    continue
                inp=inp.split()
                try:
                    var=map(int, inp)
                except:
                    print "invalid order ids"
                    time.sleep(2)
                    continue
                print "Enter a pickUpTime in 'YY-mm-dd HH:MM:SS' format. otherwise press enter to add null"
                pickupdate=raw_input("Your input: ")
                if pickupdate=='':
                    AGENT.set_delivery(var)
                    print "Addded to delivery!"
                else:
                    try:
                        pickUpTime=datetime.strptime(pickupdate, "%Y-%m-%d %H:%M:%S")
                    except:
                        print "date entered is not is specified format"
                        time.sleep(2)
                        continue
                    AGENT.set_delivery(var, pickUpTime=pickUpTime)
                    print "Added to delivery!"


        if state=="update delivery":
            res=AGENT.view_orders()
            print "--------------deliveries------------------"
            counter = -1
            for i in res[1]:
                counter+=1
                print counter, i
            while True:
                print "Enter a valid index to update delivery. otherwise press 'b' to go back"
                inp=raw_input("Your input: ")
                if inp=='b':
                    state="agent login success menu"
                    break
                if inp=='':
                    continue
                try:
                    index=int(inp)
                except:
                    continue
                if index>counter:
                    print 'index out of range'
                    continue
                if index>=0 and index<=counter:
                    vdr=AGENT.view_delivery(res[1][index][0])
                    counter2=-1
                    for j in vdr:
                        counter2+=1
                        print counter2, j
                    while True:
                        print "Enter the index of the orders to change delivery. or press 'b' to go back"
                        inp2=raw_input("Your Input: ").lower()
                        if inp2=='b':
                            break
                        if inp2=='':
                            continue
                        try:
                            inp2=int(inp2)
                        except:
                            continue
                        if inp2>counter2:
                            print 'index out of range'
                            continue
                        if inp2>=0 and inp2<=counter2:
                            trackingNo=vdr[inp2][0]
                            oid=vdr[inp2][1]
                            print "Enter 0 to change delivery times, enter 1 to remove the order, enter 'b' to go back"
                            selection=raw_input("Your Input: ").lower()
                            if selection=='b':
                                break
                            if selection=='0':
                                while True:
                                    print "Enter pickUpTime in YY-mm-dd HH:MM:SS format or press c to cancel"
                                    pickUpTime=raw_input("Your Input: ")
                                    if pickUpTime=='c':
                                        break
                                    if pickUpTime=='':
                                        pickUpTime=None
                                    else:
                                        try:
                                            pickUpTime=datetime.strptime(pickUpTime, "%Y-%m-%d %H:%M:%S")
                                        except:
                                            print "date entered is not is specified format"
                                            time.sleep(2)
                                            continue
                                    print "Enter dropOffTime in YY-mm-dd HH:MM:SS format or press c to cancel"
                                    dropOffTime=raw_input("Your Input: ")
                                    if dropOffTime=='c':
                                        break
                                    if dropOffTime=='':
                                        dropOffTime=None
                                    else:
                                        try:
                                            dropOffTime=datetime.strptime(dropOffTime, "%Y-%m-%d %H:%M:%S")
                                        except:
                                            print "date entered is not is specified format"
                                            time.sleep(2)
                                            continue
                                    AGENT.edit_delivery_order_time(trackingNo, oid, pickUpTime=pickUpTime, dropOffTime=dropOffTime)
                                    print "delivery times changed!"
                                    break
                            if selection=='1':
                                AGENT.remove_order_from_delivery(trackingNo, oid)
                                print "removed order from delivery"
                                break

        if state=="add to stock":
            vdr=AGENT.view_carries()
            counter=-1
            for x in vdr:
                counter+=1
                print counter, x
            while True:
                print "Please select a index, or to go back press b"
                inp=raw_input("Your Input: ")
                if inp=='b':
                    state="agent login success menu"
                    break
                if inp=='':
                    continue
                try:
                    index=int(inp)
                except:
                    continue
                if index>counter:
                    print 'index out of range'
                    continue
                if index>=0 and index<=counter:
                    pid=vdr[index][1]
                    sid=vdr[index][0]
                    while True:
                        print "please enter the qty (or press enter to skip) or press b to go back"
                        inp2=raw_input("Your input: ")
                        if inp2=='b':
                            break
                        if inp2=='':
                            qty=None
                        try:
                            qty=int(inp2)
                        except:
                            continue
                        print "please enter the uprice (or press enter to skip) or press b to go back"
                        inp2=raw_input("Your input: ")
                        if inp2=='b':
                            break
                        if inp2=='':
                            uprice=None
                        try:
                            uprice=float(inp2)
                        except:
                            continue
                        AGENT.update_stock(pid, sid, qty=qty, uprice=uprice)
                        time.sleep(2)
                        break




interface()
