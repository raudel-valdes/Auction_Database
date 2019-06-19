
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Modified: 06/17/2019
Modified By: Raudel Valdes
Modification Reason: adding compatibility with python 3

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
import os
from json import loads, dumps
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
Creates the .dat file for the Bulk Loading of the Action Table
"""
def gatherAuctionsTableData(auction):
    #Table Schema -> itemID|name|started|ends|sellerID|buy_price|first_bid|number_of_bids
    auction = (
        auction['ItemID'] + columnSeparator + auction['Name'] + columnSeparator + 
        auction['Started'] + columnSeparator + auction['Ends'] + columnSeparator +
        auction['Seller']['UserID']  + columnSeparator + auction['Buy_Price'] +
        columnSeparator + auction['First_Bid'] + auction['Number_of_Bids'] + '\n'
    )

    return auction


"""
Creates the .dat file for the Bulk Loading of the Bids Table
"""
def gatherBidsTableData(auction):
    if auction['Number_of_Bids'] == '0':
        return ''
    
    bids = ''
    allBids = dumps(auction['Bids']) 
    allBids = loads(allBids) 

    #The format that every bid in allBids will have
    #{'Bid': {'Bidder': {'UserID': 'grubsak@aol.com', 'Rating': '2637', 'Location': 'Akron, Ohio', 'Country': 'USA'}, 'Time': 'Dec-12-01 04:16:20', 'Amount': '$8.50'}}
    for bid in allBids:
        bid = bid['Bid']
        bidder = bid['Bidder']

        #Changing the format of the currently, money, and time attributes for SQLite compatibility
        amount = transformDollar(bid['Amount'])
        time = transformDttm(bid['Time'])
        currently = transformDollar(auction['Currently'])

        bids += (
            bidder['UserID'] + columnSeparator +  auction['ItemID'] + columnSeparator + 
            amount + columnSeparator + currently + columnSeparator + time + '\n'
        )

    return bids


"""
Creates the .dat file for the Bulk Loading of the Users Table
"""

def gatherSellersTableData(auction):
    seller = (
        auction['UserID'] + columnSeparator + auction['Rating'] + 
        columnSeparator + auction['Location'] + columnSeparator + auction['Country'] + '\n'
    )

    if auction['Number_of_Bids'] == '0':
        return seller
        
    allBids = dumps(auction['Bids']) 
    allBids = loads(allBids) 

    #The format that every bid in allBids will have
    #{'Bid': {'Bidder': {'UserID': 'grubsak@aol.com', 'Rating': '2637', 'Location': 'Akron, Ohio', 'Country': 'USA'}, 'Time': 'Dec-12-01 04:16:20', 'Amount': '$8.50'}}
    for bid in allBids:
        bid = bid['Bid']
        bidder = bid['Bidder']
        sellerExists = True

        #If either attribute (location or country) is not found then set
        # sellerExists to false and don't attatch info to seller
        try:
            bid['Location']
            bidder['Country']
        except KeyError:
            sellerExists = False
            
        if sellerExists:
            seller += (
                bidder['UserID'] + columnSeparator +  bidder['Rating'] + 
                columnSeparator + bidder['Location'] + columnSeparator + bidder['Country'] + '\n'
            )

    return seller


def gatherBiddersTableData(auction):
    bidders = ''

    if auction['Number_of_Bids'] == '0':
        return bidders
        
    allBids = dumps(auction['Bids']) 
    allBids = loads(allBids) 

    #The format that every bid in allBids will have
    #{'Bid': {'Bidder': {'UserID': 'grubsak@aol.com', 'Rating': '2637', 'Location': 'Akron, Ohio', 'Country': 'USA'}, 'Time': 'Dec-12-01 04:16:20', 'Amount': '$8.50'}}
    for bid in allBids:
        bid = bid['Bid']
        bidder = bid['Bidder']

        try:
            bidder['Location']
        except KeyError:
            bidder['Location'] = 'NULL'        

        try:
            bidder['Country']
        except KeyError:
            bidder['Country'] = 'NULL'

        bidders += (
            bidder['UserID'] + columnSeparator +  bidder['Rating'] + 
            columnSeparator + bidder['Location'] + columnSeparator + bidder['Country'] + '\n'
        )

    return bidders


"""
Creates the .dat file for the Bulk Loading of the Categories Table
"""
def gatherCategoriesTableData(auction, allCategories):
    categories = ''

    # Table Schema -> itemID|category
    for category in allCategories: 
        categories += (auction['ItemID'] + columnSeparator + category + '\n')
    
    return categories 


"""
Creates the .dat file for the Bulk Loading of the Items Table
"""
def gatherItemsTableData(auction):
    return 'Empty For Now!'


"""
1) Creating .dat files if they don't exist
2) Writing new data to the files
3) Closing the files
"""
def createTableDATFiles(auctions, bids, categories, items, sellers, bidders): 
    #Auction File
    auctionTable = open('auctionTable.txt','w')
    auctionTable.write(auctions)
    auctionTable.close()

    #Bids File
    bidsTable = open('bidsTable.txt', 'w')
    bidsTable.write(bids)        
    bidsTable.close()

    #Categories File
    categoriesTable = open('categoriesTable.txt', 'w')
    categoriesTable.write(categories)
    categoriesTable.close()

    #Items File        
    itemsTable = open('itemsTable.txt', 'w')
    itemsTable.write('Empty For Now!')
    itemsTable.close()

    #Sellers File
    sellersTable = open('sellersTable.txt', 'w')
    sellersTable.write(sellers)
    sellersTable.close()

    #Bidders File
    biddersTable = open('biddersTable.txt', 'w')
    biddersTable.write('Empty For Now!')
    biddersTable.close()

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        jsonItems = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        #initializing variables 
        auctions = ''
        bids = ''
        users = ''
        categories  = ''
        allCategories = []
        items = ''
        sellers = ''
        bidders = ''
    
        #an array that contains all of the attributes that the tables will have
        attributesArray = [
            'ItemID',
            'Name',
            'Started',
            'Seller',
            'First_Bid',
            'Number_of_Bids', 
            'Buy_Price', 
            'Amount',
            'Currently',
            'Time',
            'Rating',
            'UserID', #going to show up as null fix it
            'Role'
        ]

        for item in jsonItems:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            
            #takes  care of adding 'NULL' to any attribute that does not show up in the item obj
            for attribute in attributesArray:
                try:
                    item[attribute]
                except KeyError:
                    item[attribute]='NULL'

                    if attribute == 'Category':
                        allCategories.extend(item[attribute])

                    pass

            #gathering the necessary data for populating the auction table
            auctions += gatherAuctionsTableData(item)
            bids += gatherBidsTableData(item)
            categories += gatherCategoriesTableData(item, allCategories)
            items += gatherItemsTableData(item)
            sellers += gatherSellersTableData(item)
            bidders += gatherBiddersTableData(item)
            pass

        createTableDATFiles(auctions, bids, categories, items, sellers, bidders)


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
