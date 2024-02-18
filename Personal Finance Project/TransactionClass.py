#Class for transaction object

class Transaction():

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


