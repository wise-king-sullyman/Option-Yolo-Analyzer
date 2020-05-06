import csv
import os
from tkinter.filedialog import askopenfilename

#get input from user
fileToOpen = 'C:\\...\\YoloRecord.csv' #askopenfilename()

def csvToList(csvFile):
    csvList = []
    with open(csvFile) as csvfile:
        fileReader = csv.reader(csvfile)
        for row in fileReader:
            csvList.append(row)
        print(csvList)
        return csvList

#narrow down all order to only the orders that match the users input
def returnMatchingOrders(csvFile, expiration, ticker, optionType, strike):
    matchingOrders = []
    for row in csvToList(csvFile):
        if row[1] == expiration and row[2] == ticker and row[3] == optionType and row[7] == strike:
            matchingOrders.append(row)
    print(matchingOrders)
    return matchingOrders

#arrange orders that match criteria into buy or sell buckets, also aggregate number of contracts
def sortOrderList(orderList):
    contractList = []
    buyList = []
    sellList = []
    for order in orderList:
        buyOrSell = order[4]
        extension = float(order[8])
        contracts = int(order[5])
        if buyOrSell == 'Buy':
            buyList.append(extension)
            contractList.append(contracts)
        elif buyOrSell == 'Sell':
            sellList.append(extension)
        else:
            print('data corrupt')
            pass

    return {'contractList': contractList, 'buyList': buyList, 'sellList': sellList}

#perform math and give main dictionary of info to print
def returnTotals(sortedOrderList):
    totalContracts = sum(sortedOrderList['contractList'])
    averageBuy = (sum(sortedOrderList['buyList']) / totalContracts) / 100
    averageSell = (sum(sortedOrderList['sellList']) / totalContracts) / 100

    return {'totalContracts': totalContracts, 'averageBuy': averageBuy, 'averageSell': averageSell}

def yoloRecordSearch(fileToOpen):
    expiration = str(input("Expiration date? "))
    ticker = (input("Ticker? ")).upper()
    optionType = str(input("Put or Call? "))
    strike = str(input("Strike? "))

    #sanitize inputs
    if expiration[-4:] != 2020:
        expiration = expiration + '/2020'

    if optionType != 'Put' and optionType != 'Call':
        if optionType == 'P' or optionType == 'p':
            optionType = 'Put'
        elif optionType == 'C' or optionType == 'c':
            optionType = 'Call'

    if strike[-3:] != ('.00' or '.50'):
        strike = strike + '.00'

    try:
        matchingOrders = returnMatchingOrders(fileToOpen, expiration, ticker, optionType, strike)
        sortedOrderList = sortOrderList(matchingOrders)
        totals = returnTotals(sortedOrderList)
        print(f"\n Total Contracts: {totals['totalContracts']}")
        print(f"Average Buy Price: {totals['averageBuy']}")
        print(f"Average Sell Price: {totals['averageSell']}")
    except ZeroDivisionError:
        print("No contracts found matching descriptors")

    print("\n Press enter to close or r to repeat")
    closeOrRepeat = input()
    if closeOrRepeat == 'r':
        yoloRecordSearch(fileToOpen)

yoloRecordSearch(fileToOpen)

