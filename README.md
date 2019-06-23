# Auction Base Database

For this project I was provided a set of if JSON files that contained data from eBay auctions. The data was scrapped from eBay over ten years ago and was cleaned up in order to allow parsing through the files and accessing specific data.

The purpose of the project was to design a database that would store all of the information that was contained within the JSON files in an appropriate way.
This required the creation of a database ER MODEL to construct db tables as well as their schemas. 

In order to pass all of the data inside of the JSON files into the SQLite database I had to create a Python parser. The python parser reads through the JSON files and sends specific data to specific .dat files. These specific .dat files are structred using a delimeter, " | ", that sperates each line of data into the attributes that match the schema of the the database tables.

After the .dat files are created, there is a SQL script that gets ran and sets up the database and all of its tables. Theres also another .txt file with commands that loads all of trhe .dat file data into the database. This method is called Bulk Loading which helps transfer a lot of data to your database very quickly. This method is much more quicker and efficient than doing and INSERT for every row of data that you may have.

For this project, I also made 7 SQL queries that are used on the databse that created to answer the following questions:
1. Find the number of users in the database.
2. Find the number of users from New York (i.e., users whose location is the string ”New York”). 3. Find the number of auctions belonging to exactly four categories.
4. Find the ID(s) of auction(s) with the highest current price.
5. Find the number of sellers whose rating is higher than 1000.
6. Find the number of users who are both sellers and bidders.
7. Find the number of categories that include at least one item with a bid of more than $100.

Finally, I made the whole process more automated by creating a shell script that executes all of the  neccessary files and calls of the queries at the same time.

# Instructions to AUTOMATICALLY run the project
These Instructions assume that you have sqlite3 and Python 3 Installed on your system. Your OS must be running some type of Linux flavor.

Navigate through your terminal to the folder "Supporting Files" and call ./runParser.sh to execute all of the python scripts and database files at the same time.

# Instructions to MANUALLY run the project
These Instructions assume that you have sqlite3 and Python 3 Installed on your system.

Navigate through your terminal to the folder "Supporting Files" and run the following commands in the order that follows:
1) python my_modified_skeleton_parser.py ../ebay_data/items-*.json
2) sqlite3 AuctionBase.db < create.sql
3) sqlite3 AuctionBase.db < load.txt
4) sqlite3 AuctionBase.db < query1.sql
5) sqlite3 AuctionBase.db < query2.sql
6) sqlite3 AuctionBase.db < query3.sql
7) And so on to query 7...

# CREDITS
This project was provided by Standford University CS-145 course and given to me as an assignment by my CECS-535 Intro to Databases course at the University of Louisville during my undergraduate career.