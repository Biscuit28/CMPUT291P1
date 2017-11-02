drop table if exists deliveries;
drop table if exists olines;
drop table if exists orders;
drop table if exists customers;
drop table if exists carries;
drop table if exists products;
drop table if exists categories;
drop table if exists stores;
drop table if exists agents;

create table agents (
  aid           text,
  name          text,
  pwd       	text,
  primary key (aid));
create table stores (
  sid		int,
  name		text,
  phone		text,
  address	text,
  primary key (sid));
create table categories (
  cat           char(3),
  name          text,
  primary key (cat));
create table products (
  pid		char(6),
  name		text,
  unit		text,
  cat		char(3),
  primary key (pid),
  foreign key (cat) references categories);
create table carries (
  sid		int,
  pid		char(6),
  qty		int,
  uprice	real,
  primary key (sid,pid),
  foreign key (sid) references stores,
  foreign key (pid) references products);
create table customers (
  cid		text,
  name		text,
  address	text,
  pwd		text,
  primary key (cid));
create table orders (
  oid		int,
  cid		text,
  odate		date,
  address	text,
  primary key (oid),
  foreign key (cid) references customers);
create table olines (
  oid		int,
  sid		int,
  pid		char(6),
  qty		int,
  uprice	real,
  primary key (oid,sid,pid),
  foreign key (oid) references orders,
  foreign key (sid) references stores,
  foreign key (pid) references products);
create table deliveries (
  trackingNo	int,
  oid		int,
  pickUpTime	date,
  dropOffTime	date,
  primary key (trackingNo,oid),
  foreign key (oid) references orders);
