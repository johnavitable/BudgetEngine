import be
import pprint as pp
from bson import ObjectId

def insertExpense(acctID, DayOfMonth, Name, Amount, StartDate, EndDate):
    filter = {"Name":Name}
    expCheck =  be.expenses.count_documents(filter, limit=1)
    if expCheck == 1:
        print("Expense already exists, please review for validity")
    elif expCheck < 1:
        print("Expense does not exist. Will write to DB.")
        expenseToWrite = {
        "acctID" : acctID,
        "DayOfMonth" : DayOfMonth,
        "Name" : Name,
        "Amount" : Amount,
        "StartDate" : StartDate,
        "EndDate" : EndDate,
        "LastPostedDate": StartDate
        }
        x = be.expenses.insert_one(expenseToWrite)
        print(x.inserted_id)


actions = [
    "1: Print all expenses for account",
    "2: Print expenses for all accounts",
    "3: Set LastPostedDate",
    "4: Create new expense",
    "5: Add end date to expense",
    "6: Change amount",
    "7: Delete expense"
]

def expMenu():
    continueExpLoop = 1
    while continueExpLoop == 1:
        action = be.menuGen(actions,"Expense menu",0)
        if action == 'Q':
            continueExpLoop = 0
        if action == '1':
            be.printAsDataFrame(be.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            be.printAsDataFrame(be.listExpenses(inputacctID))
        if action == '2':
            be.printAsDataFrame(be.listCollection('expenses'))
        if action == '3':
            currExp = be.expense(input("Please enter the name of the expense you would like to update: "))
            iterNextDate = be.txIterate('Monthly',currExp.LastPostedDate)
            newDateConf = input("Is the new LastPostedDate %s? (y/n)" % iterNextDate)
            if newDateConf == 'y': currExp.setLastPostedDate(iterNextDate)
            if newDateConf == 'n': currExp.setLastPostedDate(be.convDate(input("Please enter the new LastPostedDate (YYYY-MM-DD)")))
        if action == '4':
            print("Please enter info for new expense:")
            be.printAsDataFrame(be.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            continueNewExpLoop = 1
            while continueNewExpLoop == 1:
                inputName = input("Please enter name of new expense: ")
                inputAmount = input("Please enter the amount: ")
                AmountInt = float(inputAmount)
                inputStartDate = input("Please enter a start date (YYYY-MM-DD): ")
                StartDateFormatted = be.convDate(inputStartDate)
                DayOfMonth = StartDateFormatted.day
                print("Interpreting DayOfMonth as %s from StartDate " % StartDateFormatted.day)
                inputEndDate = input("Please enter the EndDate (if applicable): ")
                if inputEndDate == "":
                    EndDateFormatted = None
                elif inputEndDate != "":
                    EndDateFormatted = be.convDate(inputEndDate)
                insertExpense(inputacctID,DayOfMonth,inputName,AmountInt,StartDateFormatted,EndDateFormatted)
                if input("Another expense in same account? (y/n): ") not in ('y','Y'):
                    continueNewExpLoop = 0
        if action == '5':
            currExp =  be.expense(input("Please enter name of expense that you wish to modify: "))
            print("Expense selected: ",currExp.name)
            EndDate = input("Please enter the desired end date for expense (YYYY-MM-DD) : ")
            currExp.addEndDate(EndDate)
        if action == '6':
            currExp =  be.expense(input("Please enter name of expense that you wish to modify: "))
            print("Expense selected: ",currExp.name)
            newAmount = float(input("Please enter the new amount for the expense (XX.XX) : "))
            currExp.changeAmount(newAmount)
        if action == '7':
            be.printAsDataFrame(be.listCollection('expenses'))
            delExpID = input("Please enter the _id of the expense to be deleted: ")
            deleteExpense(delExpID)

def deleteExpense(delExpID):
    x = be.expenses.delete_one({"_id":ObjectId(delExpID)})
    print(x.deleted_count, " documents deleted.")