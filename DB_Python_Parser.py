import os
import sys
from json import loads
from re import sub

scriptPath = os.path.dirname(os.path.realpath(__file__))
dataPath = 'ebay_data/items-0.json'
fullPath = os.path.join(scriptPath,dataPath)

dataFile = open(fullPath,'r')
dataSet = dataFile.read()
dataFile.close()

print(dataSet.ItemID)