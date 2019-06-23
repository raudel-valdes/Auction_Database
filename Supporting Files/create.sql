DROP TABLE IF EXISTS AUCTIONS;
DROP TABLE IF EXISTS SELLERS;
DROP TABLE IF EXISTS BIDDERS;
DROP TABLE IF EXISTS BIDS;
DROP TABLE IF EXISTS ITEMS;
DROP TABLE IF EXISTS CATEGORIES;

-- Table Schema -> itemID|name|started|ends|sellerID|buy_price|first_bid|number_of_bids
CREATE TABLE AUCTIONS (
  itemID INTEGER,
  name VARCHAR,
  auct_started DATETIME,
  auct_ends DATETIME,
  sellerID VARCHAR,
  buy_price FLOAT,
  first_bid FLOAT,
  current_price FLOAT,
  number_bids INTEGER,
  PRIMARY KEY (itemID)
  FOREIGN KEY (itemID) REFERENCES ITEMS (userID)
);

-- Table Schema -> userID|user_role|rating|user_location|country
CREATE TABLE SELLERS (
  userID VARCHAR,
  rating INTEGER,
  user_location VARCHAR,
  country VARCHAR,
  PRIMARY KEY (userID)
);

-- Table Schema -> userID|user_role|rating|user_location|country
CREATE TABLE BIDDERS (
  userID VARCHAR,
  rating INTEGER,
  user_location VARCHAR,
  country VARCHAR,
  PRIMARY KEY (userID)
);

-- Table Schema -> itemID|sellerID|item_description
CREATE TABLE ITEMS (
  itemID VARCHAR,
  sellerID VARCHAR,
  item_description INTEGER,
  PRIMARY KEY (itemID)
);

-- Table Schema -> itemID|category
CREATE TABLE CATEGORIES (
  itemID INTEGER,
  category VARCHAR,
  PRIMARY KEY (itemID, category)
);

-- Table Schema -> bidderID|ItemID|amount|current_bid|bid_time
CREATE TABLE BIDS (
  bidderID VARCHAR,
  itemID INTEGER,
  amount FLOAT,
  current_bid FLOAT,
  bid_time DATETIME,
  PRIMARY KEY (bidderID, itemID, amount),
  FOREIGN KEY (bidderID) REFERENCES SEllERS (userID),
  FOREIGN KEY (bidderID) REFERENCES BIDDERS (userID)
);
