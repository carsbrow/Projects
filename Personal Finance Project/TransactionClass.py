#Class for transaction object

class Transaction(): 
    """A object made to represent a transaction from a bank statement csv

        Attributes:
            date (str): The date of the transaction
            ammount (float): The ammount of the transaction
            category (str): The category of the transaction
            description (str): The description of the transaction
            type (str): The type of the transaction

        Methods:
            getter methods for each attribute
    """

    def __init__(self, date, ammount, category, description, type=""):

        self.date = date #String "mm/dd/yyyy"
        self.ammount = ammount #Decimal, transaction ammount
        self.category = category #String (Income, Food, Subscriptions, Transport & Travel, Loans, Tuition, Other)
        self.description = description #String, what the transaction was
        self.type = type #String (Purchase, Recurring, Transfer, Deposit)

    def getDate(self):
        return self.date
    
    def getAmmount(self):
        return self.ammount
    
    def getCategory(self):
        return self.category
    
    def getDescription(self):
        return self.description
    
    def getType(self):
        return self.type


