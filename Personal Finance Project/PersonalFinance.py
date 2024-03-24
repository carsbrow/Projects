import gspread
import re
from TransactionClass import Transaction



def spendingData(file_path):
    """Reads transaction data from a CSV file"""
    
    allTransactions = []
    
    with open(file_path, "r") as file:
        for line in file:
            temp = line[0:-12]  # Removing unnecessary information
            data = temp.strip().replace('"', '').split(",")

            transacDay = data[0]
            transacAmount = float(data[1])
            transacType = find_type(data[4])
            transacDescription = find_description(data[4])
            transacCategory = find_category(transacAmount, transacDescription)
            
            transacObj = Transaction(transacDay, transacAmount, transacCategory, transacDescription, transacType)
            
            allTransactions.append(transacObj)

    return allTransactions


def find_type(descriptionString):
    """Establishes the type attribute from the bank's description string"""
    
    if "PURCHASE" in descriptionString:
        transacType = "Purchase"
    elif "RECURRING" in descriptionString:
        transacType = "Recurring"
    elif "TRANSFER" in descriptionString:
        transacType = "Transfer"
    elif "DEPOSIT" in descriptionString:
        transacType = "Deposit"
    else:
        transacType = ""

    return transacType


def find_description(descriptionString):
    """Extracts the description from the bank's description string"""
    
    pattern = r'ON \d{1,2}/\d{1,2} (.+?) \w{1}\d{6,}'  # Pattern recognizes the date and concludes at routing number

    match = re.search(pattern, descriptionString)  # Searches for pattern in the description string

    if match:
        description = match.group(1)
    elif "TRANSFER" in descriptionString:
        description = "Money Transfer"
    else:
        description = ""

    return description


def find_category(amount, description):
    """Categorizes transactions based on amount and description"""
    
    lower_descr = description.lower()
    
    food_keywords = ["mcdon", "taco", "lao", "chick-fil", "chipotle", "starbucks", "coffee", "food", "qdoba", 
                     "hyve", "target", "walm", "d.p.", "brueg", "walg", "crisp", "noodles", "korean", "nashville", 
                     "afro deli", "sandwich", "bonchon", "culver"]
    
    transport_keywords = ["gas", "train", "metro", "light rail", "transit", "transport"]

    tuition_keywords = ["tuition", "college"]

    loans_keywords = []

    if amount > 0:
        return "Income"
    elif any(keyword in lower_descr for keyword in food_keywords):
        return "Food"
    elif any(keyword in lower_descr for keyword in transport_keywords):
        return "Transport & Travel"
    elif any(keyword in lower_descr for keyword in tuition_keywords):
        return "Tuition"
    elif any(keyword in lower_descr for keyword in loans_keywords):
        return "Loans"
    else:
        return "Other"


def push_data(csv_file_path, month):
    """Pushes transaction data to a Google Sheets spreadsheet"""
    
    gc = gspread.service_account()
    sh = gc.open("Personal Finances")
    wks = sh.worksheet(month)

    transactions = spendingData(csv_file_path)

    row = 8
    for transac in transactions:
        temp_data = [[transac.getDate(), transac.getAmount(), transac.getCategory(), transac.getDescription()]]
        wks.insert_rows(temp_data, row)

        if transac.getCategory() == "Income":
            wks.format(f"B{row}", {"backgroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}})
        else:
            wks.format(f"B{row}", {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}})
        
        row += 1
