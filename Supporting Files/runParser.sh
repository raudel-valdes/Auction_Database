#!/bin/bash

clear
python my_modified_skeleton_parser.py ../ebay_data/items-*.json
sqlite3 AuctionBase.db < create.sql
sqlite3 AuctionBase.db < load.txt
echo "1. Find the number of users in the Database."
sqlite3 AuctionBase.db < query1.sql
echo "2. Find the number of users from New York (i.e., users whose location is the string ”New York”)."
sqlite3 AuctionBase.db < query2.sql
echo "3. Find the number of auctions belonging to exactly four categories."
sqlite3 AuctionBase.db < query3.sql
echo "4. Find the ID(s) of auction(s) with the highest current price."
sqlite3 AuctionBase.db < query4.sql
echo "5. Find the number of sellers whose rating is higher than 1000."
sqlite3 AuctionBase.db < query5.sql
echo "6. Find the number of users who are both sellers and bidders."
sqlite3 AuctionBase.db < query6.sql
echo "7. Find the number of categories that include at least one item with a bid of more than 100 dollars."
sqlite3 AuctionBase.db < query7.sql
