import gspread
import re
from TransactionClass import Transaction



def spendingData(file_path):
    """Reads transaction data from a CSV file

        Parameters:
            file_path (str): The path to the CSV file containing transaction data
    
        Returns:
            list: A list of Transaction objects
    
    """
    
    allTransactions = []
    
    with open(file_path, "r") as file:
        for line in file: # Creating a list of Transaction objects to later add to a Google Sheets spreadsheet
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
    """Extracts the description from the bank's description string
    
        Parameters:
            descriptionString (str): The transaction's entire description string
            
        Returns:
            str: The transaction's specific description
    """
    
    pattern = r'ON \d{1,2}/\d{1,2} (.+?) \w{1}\d{6,}'  # Pattern recognizes the date and concludes at routing number

    match = re.search(pattern, descriptionString)  # Searches for pattern in the description string

    if match:
        description = match.group(1)
    elif "TRANSFER" in descriptionString: # Cannot reconize a transfer with RE so manually set description
        description = "Money Transfer"
    else:
        description = "" # If no match is found, return an empty string

    return description


def find_category(amount, description):
    """Categorizes transactions based on amount and description
    
        Parameters:
            amount (float): The transaction's amount to check if it's an income or expense
            description (str): The transaction's description, description from find_description()
            
        Returns:
            str: The transaction's category
    """
    
    lower_descr = description.lower()
    
    food_keywords = ["mcdon", "taco", "lao", "chick-fil", "chipotle", "starbucks", "coffee", "food", "qdoba", 
                     "hyve", "target", "walm", "d.p.", "brueg", "walg", "crisp", "noodles", "korean", "nashville", 
                     "afro deli", "sandwich", "bonchon", "culver"] # Keywords to identify food transactions
    
    transport_keywords = ["gas", "train", "metro", "light rail", "transit", "transport"]

    tuition_keywords = ["tuition", "college"]

    loans_keywords = []

    if amount > 0: # Assigns a category based on the transaction's amount and description
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
    """Pushes transaction data to a Google Sheets spreadsheet using gspread
    
        Parameters:
            csv_file_path (str): The path to the CSV file containing transaction data
            month (str): The month to push the data to in the Google Sheets spreadsheet
            
        Returns:
            None
    """
    
    gc = gspread.service_account() # Connecting to the API with key on local machine
    sh = gc.open("Personal Finances") # Name of the google sheet
    wks = sh.worksheet(month) # Opening the correct tab of the sheet

    transactions = spendingData(csv_file_path) # Getting the list of transactions from the CSV file

    row = 8
    for transac in transactions: 
        temp_data = [[transac.getDate(), transac.getAmount(), transac.getCategory(), transac.getDescription()]] # Nested list of data
        wks.insert_rows(temp_data, row) # Adding the data into row 8 and down

        if transac.getCategory() == "Income": # Color green if incone or red if expense
            wks.format(f"B{row}", {"backgroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}})
        else:
            wks.format(f"B{row}", {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}})
        
        row += 1
