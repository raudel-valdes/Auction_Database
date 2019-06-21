DROP TABLE IF EXISTS AUCTIONS;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS BIDS;
DROP TABLE IF EXISTS ITEMS;
DROP TABLE IF EXISTS CATEGORIES

  -- #Table Schema -> itemID|name|started|ends|sellerID|buy_price|first_bid|number_of_bids
CREATE TABLE AUCTIONS (
  itemID INTEGER,
  item_name VARCHAR,
  began DATETIME,
  ends DATETIME,
  sellerID INTEGER,
  buy_price FLOAT,
  first_bid FLOAT,
  number_of_bids INTEGER
  PRIMARY KEY (itemID)),
  FOREIGN KEY (contact_id) REFERENCES contacts (contact_id) 
  ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (group_id) REFERENCES groups (group_id) 
  ON DELETE CASCADE ON UPDATE NO ACTION
);