-- Data prepared by CMPUT 291 TAs
-- Published after the assignments are marked

-- First, Let's delete existing data:

PRAGMA foreign_keys = ON;

delete from deliveries;
delete from olines;
delete from orders;
delete from carries;
delete from customers;
delete from stores;
delete from products;
delete from categories;
delete from agents;


--Now, Let's insert some test data:

INSERT INTO categories VALUES('dai','dairy');
INSERT INTO categories VALUES('bak','Bakery');
INSERT INTO categories VALUES('mea','Meat and seafood');
INSERT INTO categories VALUES('bev','Beverages ');
INSERT INTO categories VALUES('can','Canned Goods ');
INSERT INTO categories VALUES('dry','Dry Goods ');
INSERT INTO categories VALUES('cle','Cleaners');
INSERT INTO categories VALUES('per','Personal Care');


INSERT INTO products VALUES('p10','4L milk 1%','ea','dai');
INSERT INTO products VALUES('p20','dozen large egg','ea','dai');
INSERT INTO products VALUES('p30','cream cheese','ea','dai');
INSERT INTO products VALUES('p40','400g coffee','ea','bev');
INSERT INTO products VALUES('p50','1.5L orange juice','ea','bev');
INSERT INTO products VALUES('p60','600g lean beef','ea','mea');
INSERT INTO products VALUES('p70','500g poultry','ea','mea');
INSERT INTO products VALUES('p80','1L detergent','ea','cle');
INSERT INTO products VALUES('p90','300ml dishwashing liquid','ea','cle');
INSERT INTO products VALUES('p100','400ml canned beef ravioli','ea','can');
INSERT INTO products VALUES('p110','500ml canned noodle soup','ea','can');


INSERT INTO stores VALUES(10,'Canadian Tire','780-111-2222','Edmonton South Common');
INSERT INTO stores VALUES(20,'Canadian Superstore','780-111-3333','Edmonton South Common');
INSERT INTO stores VALUES(30,'Walmart','587-111-222','Edmonton Westmount');
INSERT INTO stores VALUES(40,'Save-On-Foods','780-333-444','101-109 St NW');
INSERT INTO stores VALUES(50,'No Frills','780-444-555','104-80 Ave');
INSERT INTO stores VALUES(60,'Safeway','780-555-666','109-82 Ave');
INSERT INTO stores VALUES(70,'Organic Market','780-666-777','110-83 Ave');
INSERT INTO stores VALUES(80,'lucky 97','780-666-777','56-132 St NW');


INSERT INTO customers VALUES('c10','davood','CS Dept,University of Alberta', 00000000);
INSERT INTO customers VALUES('c20','John Doe','111-222 Ave', 00000001);
INSERT INTO customers VALUES('c30','peter','102-83 Ave', 00000002);
INSERT INTO customers VALUES('c40','Jessica','101-54 St NW', 00000003);
INSERT INTO customers VALUES('c50','Allen','4520-9569 Vegas Rd NW', 00000004);
INSERT INTO customers VALUES('c60','Paul','105-74 Ave', 00000005);
INSERT INTO customers VALUES('c70','Ashley','78-23 Ave', 00000006);
INSERT INTO customers VALUES('c80','Emma','96-89 St NW', 00000007);
INSERT INTO customers VALUES('c90','Mia','87 Strathearn Crescent NW', 00000008);
INSERT INTO customers VALUES('c100','Oliver','91 Saskatchewan Dr', 00000009);

INSERT INTO agents VALUES('a10', 'Joshua', 10000000);
INSERT INTO agents VALUES('a20', 'Harry', 10000001);
INSERT INTO agents VALUES('a30', 'Oliver', 10000002);
INSERT INTO agents VALUES('a40', 'Emily', 10000003);
INSERT INTO agents VALUES('a50', 'Peter', 10000004);
INSERT INTO agents VALUES('a60', 'Jessica', 10000005);

INSERT INTO carries VALUES(20,'p10',100,4.7);
INSERT INTO carries VALUES(20,'p20',80,2.6);
INSERT INTO carries VALUES(10,'p10',60,5.5);
INSERT INTO carries VALUES(30,'p10',100,4.5);
INSERT INTO carries VALUES(10,'p30',20,3.5);
INSERT INTO carries VALUES(40,'p40',50,5);
INSERT INTO carries VALUES(40,'p70',70,9);
INSERT INTO carries VALUES(60,'p50',65,5);
INSERT INTO carries VALUES(50,'p10',100,6.5);
INSERT INTO carries VALUES(50,'p90',150,6);
INSERT INTO carries VALUES(20,'p80',90,7);
INSERT INTO carries VALUES(40,'p30',45,5);


INSERT INTO orders VALUES(100,'c10','2017-09-26','Athabasca Hall, University of Alberta');
INSERT INTO orders VALUES(120,'c20','2017-09-26','111-222 Ave');
INSERT INTO orders VALUES(110,'c30',date('now','-5 day'),'134-53 Ave');
INSERT INTO orders VALUES(130,'c30',date('now','-6 day'),'134-53 Ave');
INSERT INTO orders VALUES(140,'c40',date('now','-3 day'),'75-103 St');
INSERT INTO orders VALUES(150,'c40',date('now','-2 day'),'75-103 St');
INSERT INTO orders VALUES(160,'c50',date('now','-12 day'),'102-114 St');
INSERT INTO orders VALUES(170,'c60',date('now'),'87-Jasper Ave');
INSERT INTO orders VALUES(180,'c20',date('now'),'76-102 St');
INSERT INTO orders VALUES(190,'c20',date('now'),'79-101 St');
INSERT INTO orders VALUES(200,'c80',date('now'),'105-83 Ave');


INSERT INTO olines VALUES(100,20,'p20',2,2.8);
INSERT INTO olines VALUES(120,20,'p10',1,4.7);
INSERT INTO olines VALUES(110,20,'p20',4,2.6);
INSERT INTO olines VALUES(130,10,'p10',2,3);
INSERT INTO olines VALUES(140,20,'p20',2,2.6);
INSERT INTO olines VALUES(140,30,'p10',6,5.5);
INSERT INTO olines VALUES(150,40,'p40',1,6);
INSERT INTO olines VALUES(150,40,'p70',1,10);
INSERT INTO olines VALUES(150,60,'p50',2,4.3);
INSERT INTO olines VALUES(160,50,'p10',2,6);
INSERT INTO olines VALUES(160,50,'p90',1,6);
INSERT INTO olines VALUES(170,20,'p80',1,7);
INSERT INTO olines VALUES(100,40,'p30',1,5);
INSERT INTO olines VALUES(160,20,'p20',1,6);
INSERT INTO olines VALUES(200,30,'p10',2,4.5);



INSERT INTO deliveries VALUES(1000,100,'2017-10-02 23:37:46',NULL);
INSERT INTO deliveries VALUES(1002,120,'2017-10-02 19:37:46','2017-10-02 23:37:46');
INSERT INTO deliveries VALUES(1003,190,datetime('now'),NULL);
INSERT INTO deliveries VALUES(1004,110,datetime('now','-4 day'),datetime('now','-3 day'));
INSERT INTO deliveries VALUES(1005,130,datetime('now','-6 day'),datetime('now','-2 day'));
INSERT INTO deliveries VALUES(1006,140,datetime('now','-2 day'),datetime('now','-1 day'));
INSERT INTO deliveries VALUES(1007,150,datetime('now','-1 day'),NULL);
INSERT INTO deliveries VALUES(1008,160,datetime('now','-6 day'),NULL);
INSERT INTO deliveries VALUES(1009,170,datetime('now'),NULL);
INSERT INTO deliveries VALUES(1010,180,datetime('now'),NULL);
