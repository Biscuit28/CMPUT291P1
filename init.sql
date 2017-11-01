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


INSERT INTO products VALUES('p1','4L milk 1%','ea','dai');
INSERT INTO products VALUES('p2','dozen large egg','ea','dai');
INSERT INTO products VALUES('p3','cream cheese','ea','dai');
INSERT INTO products VALUES('p4','400g coffee','ea','bev');
INSERT INTO products VALUES('p5','1.5L orange juice','ea','bev');
INSERT INTO products VALUES('p6','600g lean beef','ea','mea');
INSERT INTO products VALUES('p7','500g poultry','ea','mea');
INSERT INTO products VALUES('p8','1L detergent','ea','cle');
INSERT INTO products VALUES('p9','300ml dishwashing liquid','ea','cle');
INSERT INTO products VALUES('p10','400ml canned beef ravioli','ea','can');
INSERT INTO products VALUES('p11','500ml canned noodle soup','ea','can');


INSERT INTO stores VALUES('s1','Canadian Tire','780-111-2222','Edmonton South Common');
INSERT INTO stores VALUES('s2','Canadian Superstore','780-111-3333','Edmonton South Common');
INSERT INTO stores VALUES('s3','Walmart','587-111-222','Edmonton Westmount');
INSERT INTO stores VALUES('s4','Save-On-Foods','780-333-444','101-109 St NW');
INSERT INTO stores VALUES('s5','No Frills','780-444-555','104-80 Ave');
INSERT INTO stores VALUES('s6','Safeway','780-555-666','109-82 Ave');
INSERT INTO stores VALUES('s7','Organic Market','780-666-777','110-83 Ave');
INSERT INTO stores VALUES('s8','lucky 97','780-666-777','56-132 St NW');


INSERT INTO customers VALUES('c1','davood','CS Dept,University of Alberta', 00000000);
INSERT INTO customers VALUES('c2','john doe','111-222 Ave', 00000001);
INSERT INTO customers VALUES('c3','peter','102-83 Ave', 00000002);
INSERT INTO customers VALUES('c4','jessica','101-54 St NW', 00000003);
INSERT INTO customers VALUES('c5','allen','4520-9569 Vegas Rd NW', 00000004);
INSERT INTO customers VALUES('c6','paul','105-74 Ave', 00000005);
INSERT INTO customers VALUES('c7','ashley','78-23 Ave', 00000006);
INSERT INTO customers VALUES('c8','emma','96-89 St NW', 00000007);
INSERT INTO customers VALUES('c9','mia','87 Strathearn Crescent NW', 00000008);
INSERT INTO customers VALUES('c10','oliver','91 Saskatchewan Dr', 00000009);

INSERT INTO agents VALUES('a1', 'joshua', 10000000);
INSERT INTO agents VALUES('a2', 'harry', 10000001);
INSERT INTO agents VALUES('a3', 'oliver', 10000002);
INSERT INTO agents VALUES('a4', 'emily', 10000003);
INSERT INTO agents VALUES('a5', 'peter', 10000004);
INSERT INTO agents VALUES('a6', 'jessica', 10000005);

INSERT INTO carries VALUES('s2','p1',100,4.7);
INSERT INTO carries VALUES('s2','p2',80,2.6);
INSERT INTO carries VALUES('s1','p1',60,5.5);
INSERT INTO carries VALUES('s3','p1',100,4.5);
INSERT INTO carries VALUES('s1','p3',20,3.5);
INSERT INTO carries VALUES('s4','p4',50,5);
INSERT INTO carries VALUES('s4','p7',70,9);
INSERT INTO carries VALUES('s6','p5',65,5);
INSERT INTO carries VALUES('s5','p1',100,6.5);
INSERT INTO carries VALUES('s5','p9',150,6);
INSERT INTO carries VALUES('s2','p8',90,7);
INSERT INTO carries VALUES('s4','p3',45,5);


INSERT INTO orders VALUES('o1','c1','2017-09-26','Athabasca Hall, University of Alberta');
INSERT INTO orders VALUES('o2','c2','2017-09-26','111-222 Ave');
INSERT INTO orders VALUES('o3','c3',date('now','-5 day'),'134-53 Ave');
INSERT INTO orders VALUES('o4','c3',date('now','-6 day'),'134-53 Ave');
INSERT INTO orders VALUES('o5','c4',date('now','-3 day'),'75-103 St');
INSERT INTO orders VALUES('o6','c4',date('now','-2 day'),'75-103 St');
INSERT INTO orders VALUES('o7','c5',date('now','-12 day'),'102-114 St');
INSERT INTO orders VALUES('o8','c6',date('now'),'87-Jasper Ave');
INSERT INTO orders VALUES('o9','c2',date('now'),'76-102 St');
INSERT INTO orders VALUES('o10','c2',date('now'),'79-101 St');
INSERT INTO orders VALUES('o11','c8',date('now'),'105-83 Ave');


INSERT INTO olines VALUES('o1','s2','p2',2,2.8);
INSERT INTO olines VALUES('o2','s2','p1',1,4.7);
INSERT INTO olines VALUES('o3','s2','p2',4,2.6);
INSERT INTO olines VALUES('o4','s1','p1',2,3);
INSERT INTO olines VALUES('o5','s2','p2',2,2.6);
INSERT INTO olines VALUES('o5','s3','p1',6,5.5);
INSERT INTO olines VALUES('o6','s4','p4',1,6);
INSERT INTO olines VALUES('o6','s4','p7',1,10);
INSERT INTO olines VALUES('o6','s6','p5',2,4.3);
INSERT INTO olines VALUES('o7','s5','p1',2,6);
INSERT INTO olines VALUES('o7','s5','p9',1,6);
INSERT INTO olines VALUES('o8','s2','p8',1,7);
INSERT INTO olines VALUES('o1','s4','p3',1,5);
INSERT INTO olines VALUES('o7','s2','p2',1,6);
INSERT INTO olines VALUES('o11','s3','p1',2,4.5);



INSERT INTO deliveries VALUES('d1','o1','2017-10-02 23:37:46',NULL);
INSERT INTO deliveries VALUES('d2','o2','2017-10-02 19:37:46','2017-10-02 23:37:46');
INSERT INTO deliveries VALUES('d3','o10',datetime('now'),NULL);
INSERT INTO deliveries VALUES('d4','o3',datetime('now','-4 day'),datetime('now','-3 day'));
INSERT INTO deliveries VALUES('d5','o4',datetime('now','-6 day'),datetime('now','-2 day'));
INSERT INTO deliveries VALUES('d6','o5',datetime('now','-2 day'),datetime('now','-1 day'));
INSERT INTO deliveries VALUES('d7','o6',datetime('now','-1 day'),NULL);
INSERT INTO deliveries VALUES('d8','o7',datetime('now','-6 day'),NULL);
INSERT INTO deliveries VALUES('d9','o8',datetime('now'),NULL);
INSERT INTO deliveries VALUES('d10','o9',datetime('now'),NULL);
