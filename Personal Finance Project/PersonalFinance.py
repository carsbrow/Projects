

import gspread
import TransactionClass
import re


def spendingData(file_path):
    """filename as a csv file for transaction data"""
    
    with open(file_path, "r") as file:

        allTransancations = []
        
        for line in file:
            temp = line[0:-12] #removing unnecessary information
            data = temp.strip().replace('"','').split(",")

            transacDay = data[0]
            transacAmmount = float(data[1])
            transacType = findType(data[4])
            transacDescription = findDescription(data[4])
            transacCategory = findCategory(transacAmmount, transacDescription)
            
            transacObj = TransactionClass.Transaction(transacDay, transacAmmount, transacCategory, transacDescription, transacType)
            
            allTransancations.append(transacObj)

    
    return allTransancations

def findType(descriptionString):
    """establishes the type attribute from the banks description string"""
    
    if "PURCHASE" in descriptionString:
        transacType = "Purchase"
    elif "RECURRING" in descriptionString:
        transacType = "Recurring"
    elif "TRANSFER" in descriptionString:
        transacType = "Transfer"
    elif "DEPOSIT" in descriptionString:
        transacType = "Deposit"

    return transacType

def findDescription(descriptionString):
    
    pattern = r'ON \d{1,2}/\d{1,2} (.+?) \w{1}\d{6,}' #pattern, reconizes the date and concludes at rounting number

    match = re.search(pattern, descriptionString) #Searches param for pattern with re

    if match:
        description = match.group(1)
        return description
    
    elif "TRANSFER" in descriptionString:
        return "Money Transfer"
    
    else:
        return ""

def findCategory(ammount, description):
    """Categories:
        Income, Food, Subscriptions, Transport & Travel, Tuition, Loans, Other
    """
    lower_descr = description.lower()
    
    food_keyword = ["mcdon", "taco", "lao", "chick-fil", "chipotle", "starbucks", "coffee", "food", "qdoba", 
                    "hyve", "target", "walm", "d.p.", "brueg", "walg", "crisp", "noodles", "korean", "nashville", 
                    "afro deli", "sandwich", "bonchon", "culver"]
    
    transport_keyword = ["gas", "train", "metro", "light rail", "transit", "transport"]

    tuition_keyword = ["tuition", "college"]

    loans_keyword = []


    if ammount > 0:
        return "Income"
    
    elif any(keyword in lower_descr for keyword in food_keyword):
        return "Food"
    
    elif any(keyword in lower_descr for keyword in transport_keyword):
        return "Transport & Travel"

    elif any(keyword in lower_descr for keyword in tuition_keyword):
        return "Tuition"
    
    elif any(keyword in lower_descr for keyword in loans_keyword):
        return "Loans"

    else:
        return "Other"

def pushData(csvfilepath, month):

    
    gc = gspread.service_account(filename="/Users/carsonbrown/Desktop/personalfinance-414419-0fcf8ca5625b.json")
    

    sh = gc.open("Personal Finances")
    wks = sh.worksheet(f"{month}")

    transactions = spendingData(csvfilepath)

    row = 8
    for transac in transactions:
        temp_data = [[transac.getDate(), transac.getAmmount(), transac.getCategory(), transac.getDescription()]]
        wks.insert_rows(temp_data, row)

        if transac.getCategory() == "Income": #Cell background color green for income
            wks.format(f"B{row}", 
                       {"backgroundColor": {
                           "red": 0.0,
                           "green": 1.0,
                           "blue": 0.0
                       }})
            
        else:
            wks.format(f"B{row}",  #red for spending
                       {"backgroundColor": {
                           "red": 1.0,
                           "green": 0.0,
                           "blue": 0.0
                       }})
        row += 1

    
    
    
    

        
        
    


    





